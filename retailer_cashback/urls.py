from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from . import views

urlpatterns = [
    path('register-retailer', views.register_retailer, name='register_retailer'),
    path('validate-retailer', views.validate_retailer, name='validate_retailer'),
    path('register-purchase', views.register_purchase, name='register_purchase'),
    path('list-purchases', views.list_purchases, name='list_purchases'),
    path('accumulated-cashback', views.accumulated_cashback, name='accumulated_cashback'),

    #Authentication views
    path('get-token-auth/', obtain_jwt_token , name='get_token'),
    path('refresh-token-auth/', refresh_jwt_token, name='refresh_token'),
    path('verify-token-auth/', verify_jwt_token, name='verify_token'),
]
