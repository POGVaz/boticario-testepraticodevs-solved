from djmoney.money import Money

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from retailer_cashback.models import Purchase, Retailer

class TestRetailer(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            'test_username', 'email@test.com', 'test_password',
            first_name= 'test_name', last_name= 'test_surname',is_active=True)

    def test_get_full_name(self):
        '''
            Should get the retailer's full name.
        '''
        test_retailer = Retailer.objects.create(
            user= self.test_user,cpf='12345678910')

        self.assertEqual(test_retailer.full_name, 'test_name test_surname')

    def test_str(self):
        '''
            Should render the string representation of the retailer.
        '''
        test_retailer = Retailer.objects.create(
            user=self.test_user, cpf='12345678910')

        self.assertEqual(str(test_retailer), 'test_username')

class TestPurchase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            'test_username', 'email@test.com', 'test_password',
            first_name= 'test_name', last_name= 'test_surname',is_active=True)

        self.test_retailer = Retailer.objects.create(
            user=self.test_user, cpf='12345678910')

    def test_str(self):
        '''
            Should render the string representation of the retailer.
        '''
        test_purchase = Purchase.objects.create(code='test_code', purchase_date=timezone.now(
        ), status=Purchase.PurchaseStatus.EM_VALIDACAO, retailer=self.test_retailer, value=Money(1000, 'BRL'))

        self.assertEqual(str(test_purchase), 'test_code')
