from django.db import models
from django.contrib.auth.models import User

class Retailer(models.Model):
    '''
        User profile for retailers.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)

    @property
    def full_name(self):
        return (''.join([self.user.first_name, ' ', self.user.last_name]))

    def  __str__(self):
        return self.user.username
