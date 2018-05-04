import re

from django import forms
from django.core.exceptions import ValidationError

from .models import BankUser, BankAccount
from .utils import validDNI


class BankUserForm(forms.ModelForm):
    """
    BankUser form that validates only enter letter in names and also validates DNI
    """
    class Meta:
        model = BankUser
        fields = ['first_name', 'last_name', 'DNI']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError("Wrong first name, enter only letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise ValidationError("Wrong last name, enter only letters")
        return last_name

    def clean_DNI(self):
        dni = self.cleaned_data['DNI']
        if not re.compile("[0-9]{8,8}[A-Za-z]").match(dni) or not validDNI(dni):
            raise ValidationError("Wrong DNI")
        user = BankUser.objects.filter(DNI=dni)

        if user and self.instance.id != user[0].id:
            raise ValidationError("DNI already exists")
        return dni


class BankAccountForm(forms.ModelForm):
    """
    BankAccount form that validates IBAN
    """
    class Meta:
        model = BankAccount
        fields = ['IBAN']

    def clean_IBAN(self):
        data = self.cleaned_data['IBAN']

        if not re.compile("[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16}").match(data):
            raise ValidationError("Wrong IBAN")
        account = BankAccount.objects.filter(IBAN=data)

        if account:
            raise ValidationError("IBAN already exists")

        return data
