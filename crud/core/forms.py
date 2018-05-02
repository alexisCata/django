import re

from django import forms
from django.core.exceptions import ValidationError

from .models import BankUser, BankAccount


class BankUserForm(forms.ModelForm):
    class Meta:
        model = BankUser
        fields = ['first_name', 'last_name']

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


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['IBAN']

    def clean_IBAN(self):
        data = self.cleaned_data['IBAN']

        if not re.compile("[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16}").match(data):
            raise ValidationError("Wrong IBAN")

        return data
