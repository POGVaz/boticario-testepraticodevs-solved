# Business logic repository
# These functions could be broken down into files to represent their domain

from djmoney.money import Money
import requests

from django.contrib.auth.models import User

from .models import Purchase, Retailer

import logging
logger = logging.getLogger(__name__)

APPROVED_CPF_LIST = ['15350946056']

ACCUMULATED_CASHBACK_URL = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback'
ACCUMULATED_CASHBACK_TOKEN = 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'

def create_retailer(cpf, email, password, first_name, last_name):
    # Create a user for this retailer
    user = User.objects.create_user(
        username=email, email=email, password=password, first_name=first_name, last_name=last_name)
    user.save()
    # Create the retailer object with the user
    retailer = Retailer.objects.create(user=user, cpf=cpf)
    retailer.save()

    return retailer


def create_purchase(code, purchase_date, cpf, value):
    try:
        retailer = Retailer.objects.get(cpf=cpf)
    except:
        logger.error("No retailer found for cpf: {}".format(cpf))
        raise

    purchase = Purchase.objects.create(code=code, purchase_date=purchase_date,
                                       retailer=retailer, value=value)
    apply_cashback(purchase)
    set_initial_purchase_status(purchase)
    return purchase

def apply_cashback(purchase:Purchase):
    PERCENT_10 = 0.1
    PERCENT_15 = 0.15
    PERCENT_20 = 0.2
    # Check for cashback range
    if (purchase.value.amount < 1000):
        purchase.cashback_applied += PERCENT_10
        purchase.cashback_value = purchase.value*PERCENT_10
    elif (purchase.value.amount < 1500):
        purchase.cashback_applied += PERCENT_15
        purchase.cashback_value = purchase.value*PERCENT_15
    else:
        purchase.cashback_applied += PERCENT_20
        purchase.cashback_value = purchase.value*PERCENT_20

    return purchase

def set_initial_purchase_status(purchase:Purchase):
    if (purchase.retailer.cpf in APPROVED_CPF_LIST):
        purchase.status = Purchase.PurchaseStatus.APROVADA
    else:
        purchase.status = Purchase.PurchaseStatus.EM_VALIDACAO

    return purchase


def get_accumulated_cashback(retailer_cpf):
    headers = {'token': ACCUMULATED_CASHBACK_TOKEN}
    parameters = {'cpf': retailer_cpf}
    cashback_request = requests.get(ACCUMULATED_CASHBACK_URL, params=parameters, headers=headers)

    if (cashback_request.json()['statusCode'] == 200):
        return cashback_request.json()['body']['credit']
