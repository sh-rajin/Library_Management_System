from django.db import models
from django.contrib.auth.models import User
from . constants import GENDER_TYPE
# Create your models here.

class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    library_card_no = models.CharField(max_length=20, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12)

    def __str__(self):
        return self.library_card_no
    
    
class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name="address", on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.street
    
    
class DepositModel(models.Model):
    user = models.ForeignKey(UserLibraryAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    
    
    def __str__(self):
        return f'{self.user} - {self.amount}'
    
    
