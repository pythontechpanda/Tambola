from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class City(models.Model):
    city_name=models.CharField(max_length=100)
    def __str__(self):
        return self.city_name
class User(AbstractUser):
    date_of_birth=models.DateField(null=True)
    mobile_no=models.CharField(max_length=50,null=True)
    gender=models.CharField(max_length=50,null=True)
    city=models.ForeignKey(City,on_delete=models.CASCADE, null=True)
    is_verified=models.BooleanField(default=False)
    is_above18=models.BooleanField(default=False)
    