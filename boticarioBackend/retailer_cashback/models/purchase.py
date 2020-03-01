from djmoney.models.fields import MoneyField

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as label

from .retailer import Retailer

class Purchase(models.Model):
    '''
        Purchases made by retailers.
    '''
    class PurchaseStatus(models.TextChoices):
        '''
            Enumeration for each state a Purchase can be.
        '''
        EM_VALIDACAO = "EV", label('Em Validação')
        APROVADA = "AP", label('Aprovada')

        #VALIDATING = "VL", label('Validating')
        #APPROVED = "AP", label('Approved')

    code = models.CharField(max_length=200)
    purchase_date = models.DateTimeField(verbose_name='date purchased')
    status = models.CharField(max_length=200, choices=PurchaseStatus.choices, default=PurchaseStatus.EM_VALIDACAO)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    # To comply with certain strict accounting or financial regulations,
    #   one may consider using max_digits=19 and decimal_places=4
    value = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL')
    # Add cashback data to the purchase in case it is needed to query for the value
    cashback_applied = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    cashback_value = MoneyField(max_digits=14, decimal_places=2, default_currency='BRL', null=True)

    def __str__(self):
        return self.code
