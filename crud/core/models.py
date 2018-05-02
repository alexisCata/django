from django.db import models
from django.contrib.auth.models import User


class BankUser(models.Model):

    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class BankAccount(models.Model):
    bank_user = models.ForeignKey(BankUser, on_delete=models.CASCADE, name='bank_user')
    IBAN = models.CharField(max_length=140)

    def __str__(self):
        return self.IBAN
