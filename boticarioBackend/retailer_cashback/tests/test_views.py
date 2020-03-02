from rest_framework import status
from rest_framework.test import APITestCase
from djmoney.money import Money

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from retailer_cashback.models import Retailer, Purchase

from unittest import skip
import logging
logger = logging.getLogger(__name__)

class TestAuthViews(APITestCase):

    def setUp(self):
        self.get_token_url = reverse('get_token')
        self.refresh_token_url = reverse('refresh_token')
        self.verify_token_url = reverse('verify_token')
        self.client = Client()

        #Create and saves a user that gets valid tokens
        self.test_user = User.objects.create_user(
            username='user', email='user@foo.com', password='pass')
        self.test_user.save()

    def test_get_jwt_token(self):
        '''
            Should get a valid token for valid user.
        '''
        response = self.client.post(
            self.get_token_url, {'username': 'user', 'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        logger.debug("Got token: {}".format(token))

    def test_refuse_auth_invalid_user(self):
        '''
            Should send 404 response to invalid user request for JWT token.
        '''
        response = self.client.post(
            self.get_token_url, {'username': 'invalid', 'password': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refuse_jwt_inactive_user(self):
        '''
            Should send 404 response to inactive user request for JWT token.
        '''
        self.test_user.is_active = False
        self.test_user.save()

        response = self.client.post(
            self.get_token_url, {'username': 'user', 'password': 'pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @skip
    def test_refresh_jwt_token(self):
        '''
            Should obtain a valid token for valid token refresh.
        '''
        response = self.client.post(
            self.get_token_url, {'username': 'user', 'password': 'pass'}, format='json')
        token = response.data['token']
        logger.debug("Got token: {}".format(token))

        refresh_response = self.client.post(
            self.refresh_token_url, {'token': token}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in refresh_response.data)
        new_token = refresh_response.data['token']
        logger.debug("Got fresh token: {}".format(new_token))

    def test_refresh_invalid_token(self):
        '''
            Should respond with 404 for invalid token refresh.
        '''
        refresh_response = self.client.post(
            self.refresh_token_url, {'token': 'invalid_token'}, format='json')
        self.assertEqual(refresh_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_verify_valid_token(self):
        '''
            Should respond with 200 for valid token verify.
        '''
        response = self.client.post(
            self.get_token_url, {'username': 'user', 'password': 'pass'}, format='json')
        token = response.data['token']
        logger.debug("Got token: {}".format(token))

        verify_response = self.client.post(self.verify_token_url, {'token': token}, format='json')
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

    def test_verify_invalid_token(self):
        '''
            Should respond with 404 for invalid token verify.
        '''
        verify_response = self.client.post(
            self.verify_token_url, {'token': 'invalid_token'}, format='json')
        self.assertEqual(verify_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

class TestRetailerViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.authorized_user = User.objects.create_user(username='admin', password='admin')
        self.authorized_user.save()

        #Get valid token for tests
        response = self.client.post(reverse('get_token'), {
                                    'username': 'admin', 'password': 'admin'}, format='json')
        self.valid_token = response.data['token']

    def test_register_retailer(self):
        '''
            Should create a retailer, a user for that retailer and return 200.
        '''
        response = self.client.post(reverse('register_retailer'), {
                                   'email': 'user@test.com', 'password': 'pass', 'first_name': 'name', 'last_name': 'surname', 'cpf': '12345678910'}, format='json', HTTP_AUTHORIZATION='JWT '+self.valid_token)

        # Create user
        test_user = User.objects.get(email='user@test.com')
        self.assertEqual(test_user.username, 'user@test.com')
        self.assertEqual(test_user.first_name, 'name')
        self.assertEqual(test_user.last_name, 'surname')

        # Create retailer
        test_retailer = Retailer.objects.get(cpf='12345678910')
        self.assertEqual(test_retailer.user, test_user)

        #Return 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_retailer_no_token(self):
        '''
            Should return unauthorized for unauthorized access.
        '''
        response = self.client.post(reverse('register_retailer'), {'email': 'user', 'password': 'pass', 'first_name': 'name', 'last_name': 'surname', 'cpf': '12345678910'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_validate_OK_retailer(self):
        '''
            Should return 200 to authenticated users.
        '''
        response = self.client.get(
            reverse('validate_retailer'),
            {'username': 'admin', 'password': 'admin'},
            format='json', HTTP_AUTHORIZATION='JWT '+self.valid_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        logger.debug(response.body)

    def test_validate_invalid_retailer(self):
        '''
            Should return 400 to invalid users.
        '''
        response = self.client.get(
            reverse('validate_retailer'),
            {'username': 'invalid', 'password': 'invalid'},
            format='json', HTTP_AUTHORIZATION='JWT '+self.valid_token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_retailer_no_token(self):
        '''
            Should return 401 to unauthenticated users.
        '''
        response = self.client.get(reverse('validate_retailer'), {'username': 'admin', 'password': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accumulated_cashback(self):
        '''
            Should return accumulated cashback from external source.
        '''
        response = self.client.get(reverse('accumulated_cashback'), {
                                   'cpf': '12345678910'}, format='json',
                                   HTTP_AUTHORIZATION='JWT '+self.valid_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(response['body']['credit'], 4893)

    def test_accumulated_cashback_no_token(self):
        '''
            Should return 401 for unauthorized access.
        '''
        response = self.client.get(reverse('accumulated_cashback'), {
                                   'cpf': '12345678910'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestPurchaseViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.authorized_user = User.objects.create_user(
            username='admin', password='admin')
        self.authorized_user.save()

        #Get valid token for tests
        response = self.client.post(reverse('get_token'), {
                                    'username': 'admin', 'password': 'admin'}, format='json')
        self.valid_token = response.data['token']

    def test_register_purchase(self):
        '''
            Should create a purchase for the retailer with the provided cpf.
        '''
        test_user = User.objects.create_user(username='test_name', password='test_password')
        test_retailer = Retailer.objects.create(cpf='12345678910', user=test_user)

        response = self.client.post(
            reverse('register_purchase'), {'code': '123', 'value': 900, 'date': timezone.now(), 'cpf': '12345678910'}, format='json', HTTP_AUTHORIZATION='JWT '+self.valid_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_purchase = Purchase.objects.get(code='123')
        self.assertEqual(test_purchase.status, Purchase.PurchaseStatus.EM_VALIDACAO)
        self.assertEqual(test_purchase.retailer, test_retailer)
        self.assertEqual(test_purchase.value, Money(900, 'BRL'))
        self.assertEqual(test_purchase.cashback_applied, 0.1)
        self.assertEqual(test_purchase.cashback_value, Money(90, 'BRL'))

    def test_register_purchase_approved_cpf(self):
        '''
            Should create a purchase for the retailer with the provided cpf.
        '''
        test_user = User.objects.create_user(username='test_name', password='test_password')
        test_retailer = Retailer.objects.create(
            cpf='15350946056', user=test_user)

        response = self.client.post(
            reverse('register_purchase'), {'code': '123', 'value': 1200, 'date': timezone.now(), 'cpf': '15350946056'}, format='json', HTTP_AUTHORIZATION='JWT '+self.valid_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_purchase = Purchase.objects.get(code='123')
        self.assertEqual(test_purchase.status, Purchase.PurchaseStatus.APROVADA)
        self.assertEqual(test_purchase.retailer, test_retailer)
        self.assertEqual(test_purchase.value, Money(1200, 'BRL'))
        self.assertEqual(test_purchase.cashback_applied, 0.15)
        self.assertEqual(test_purchase.cashback_value, Money(180, 'BRL'))

    def test_register_purchase_no_token(self):
        '''
            Should return 401 for unauthorized access.
        '''
        response = self.client.post(reverse('register_purchase'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_purchase_list(self):
        '''
            Should return a list with all the purchases.
        '''
        # Create the purchases to list
        test_user = User.objects.create_user(username='test_name', password='test_password')
        test_retailer = Retailer.objects.create(cpf='12345678910', user=test_user)

        Purchase.objects.create(code='123', purchase_date=timezone.now(), status=Purchase.PurchaseStatus.APROVADA, retailer=test_retailer, value=Money(900, 'BRL'), cashback_applied=0.1, cashback_value=Money(90, 'BRL'))
        Purchase.objects.create(code='456', purchase_date=timezone.now(), status=Purchase.PurchaseStatus.EM_VALIDACAO, retailer=test_retailer, value=Money(1200, 'BRL'), cashback_applied=0.15, cashback_value=Money(180, 'BRL'))
        Purchase.objects.create(code='789', purchase_date=timezone.now(), status=Purchase.PurchaseStatus.EM_VALIDACAO, retailer=test_retailer, value=Money(2000, 'BRL'), cashback_applied=0.2, cashback_value=Money(400, 'BRL'))

        response = self.client.get(
            reverse('list_purchases'), HTTP_AUTHORIZATION='JWT '+self.valid_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug("Got response:" + response.data)

        self.assertEqual(response.data, [])

    def test_get_purchase_list_no_token(self):
        '''
            Should return 401 for unauthorized access.
        '''
        response = self.client.get(reverse('list_purchases'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
