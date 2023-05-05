from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    location = models.CharField(max_length=50, null=True)
    phone = models.BigIntegerField(null=True)
    is_verified = models.BooleanField(default=False)


class UserLog(models.Model):
    request_method = models.CharField(max_length=20)
    url = models.CharField(max_length=50)
    count = models.IntegerField(default=1)

