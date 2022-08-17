from django.contrib.auth.models import AbstractUser
from django.db import models

from app import settings


class User(AbstractUser):
    pass


class Coin(models.Model):
    rank = models.IntegerField()
    name = models.CharField(max_length=255, unique=True)
    symbol = models.CharField(max_length=255, unique=True)
    uuid = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    market_cap = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="coins")
    icon = models.URLField()
