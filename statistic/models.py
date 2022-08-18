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
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="coins")

    class Meta:
        ordering = ["rank"]
