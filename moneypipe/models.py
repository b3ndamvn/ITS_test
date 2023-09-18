from django.db import models
from djmoney.models.fields import MoneyField


class MoneyUser(models.Model):
    name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    INN = models.CharField(max_length=12, unique=True)
    balance = MoneyField(decimal_places=2, default_currency='RUB', max_digits=20)
