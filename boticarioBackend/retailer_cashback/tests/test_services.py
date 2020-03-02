from djmoney.money import Money

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from retailer_cashback.models import Purchase, Retailer
from retailer_cashback.services import apply_cashback, create_retailer, set_initial_purchase_status, get_accumulated_cashback

def create_test_retailer(cpf, user):
    return Retailer.objects.create(cpf=cpf, user=user)

def create_test_purchase(value, retailer):
    return Purchase.objects.create(code='test_code', purchase_date=timezone.now(), status=Purchase.PurchaseStatus.EM_VALIDACAO, retailer=retailer, value=Money(value, 'BRL'))

class TestCreateRetailer(TestCase):

    def test_create_retailer(self):
        '''
            Should create and return a retailer profile.
        '''
        test_retailer = create_retailer(cpf='12345678910', email='email@test.com', password='test_password', first_name='test_first_name', last_name='test_last_name')

        database_retailer = Retailer.objects.get(pk=test_retailer.id)
        self.assertTrue(database_retailer.cpf, '12345678910')

    def test_create_retailer_user(self):
        '''
            Should create an active user for the retailer with the same username and email.
        '''
        test_retailer = create_retailer(cpf='12345678910', email='email@test.com',
                                         password='test_password', first_name='test_first_name', last_name='test_last_name')

        test_user = test_retailer.user
        self.assertTrue(test_user.is_active)
        self.assertEqual(test_user.email, 'email@test.com')
        self.assertEqual(test_user.username, 'email@test.com')


class TestPurchaseCashback(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            'test_username', 'email@test.com', 'test_password',
            first_name='test_name', last_name='test_surname', is_active=True)

        self.test_retailer = Retailer.objects.create(cpf='12345678910', user=self.test_user)

    def test_cashback_less_than_1000(self):
        '''
            Should apply 10% cashback to the purchase.
        '''
        test_purchase = create_test_purchase(900, self.test_retailer)

        self.assertEqual(test_purchase.cashback_applied, 0)
        self.assertIsNone(test_purchase.cashback_value)

        apply_cashback(test_purchase)

        self.assertEqual(test_purchase.cashback_applied, 0.1)
        self.assertEqual(test_purchase.cashback_value, Money(90, 'BRL'))

    def test_cashback_between_1000_1500(self):
        '''
            Should apply 15% cashback to the purchase.
        '''
        test_purchase = create_test_purchase(1200, self.test_retailer)

        self.assertEqual(test_purchase.cashback_applied, 0)
        self.assertIsNone(test_purchase.cashback_value)

        apply_cashback(test_purchase)

        self.assertEqual(test_purchase.cashback_applied, 0.15)
        self.assertEqual(test_purchase.cashback_value, Money(180, 'BRL'))

    def test_cashback_more_than_1500(self):
        '''
            Should apply 20% cashback to the purchase.
        '''
        test_purchase = create_test_purchase(2000, self.test_retailer)

        self.assertEqual(test_purchase.cashback_applied, 0)
        self.assertIsNone(test_purchase.cashback_value)

        apply_cashback(test_purchase)

        self.assertEqual(test_purchase.cashback_applied, 0.2)
        self.assertEqual(test_purchase.cashback_value, Money(400, 'BRL'))


class TestSetInitialPurchaseStatus(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            'test_username', 'email@test.com', 'test_password',
            first_name='test_name', last_name='test_surname', is_active=True)

    def test_status_validating(self):
        '''
            Should set status as 'EM_VALIDACAO' most users purchases.
        '''

        test_retailer = create_test_retailer('12345678910', self.test_user)
        test_purchase = create_test_purchase(1000, test_retailer)

        set_initial_purchase_status(test_purchase)

        self.assertEqual(test_purchase.status, Purchase.PurchaseStatus.EM_VALIDACAO)

    def test_status_approved(self):
        '''
            Should set status as 'APROVADA' for specific users purchases.
        '''

        test_retailer = create_test_retailer('15350946056', self.test_user)
        test_purchase = create_test_purchase(1000, test_retailer)

        set_initial_purchase_status(test_purchase)

        self.assertEqual(test_purchase.status, Purchase.PurchaseStatus.APROVADA)

class TestAccumulatedCashback(TestCase):

    def test_get_accumulated_cashback(self):
        '''
            Should return the accumulated cashback for an external source.
        '''
        accumulated_cashback = get_accumulated_cashback('1234567810')
        #Assert that the return value is a number, since it changes:
        self.assertEqual(type(accumulated_cashback), int)
