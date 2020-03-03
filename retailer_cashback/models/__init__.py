from .purchase import Purchase
from .retailer import Retailer

# To facilitate development create default user
from django.contrib.auth.models import User
from django.conf import settings
if (settings.DEBUG and not(User.objects.filter(username='myUser').exists())):
    User.objects.create_user(username='myUser', password='myPassword')
