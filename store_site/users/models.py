from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    cash = models.FloatField(blank=True, null=True, default=settings.CASH)

