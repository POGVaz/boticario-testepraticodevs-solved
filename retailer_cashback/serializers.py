from rest_framework import serializers

from .models import Purchase, Retailer

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = ['cpf', 'user']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['code', 'purchase_date', 'status', 'retailer', 'value', 'cashback_applied', 'cashback_value']
