from django.db import models
from djmoney.models.fields import MoneyField


class MoneyUser(models.Model):
    name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    INN = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(decimal_places=2, max_digits=20)

    def check_enough_balance(self, value):
        if self.balance < float(value):
            return False
        return True
