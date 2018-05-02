from django import forms

from .models import BankUser


class BankUserForm(forms.ModelForm):
    class Meta:
        model = BankUser
        fields = ['first_name', 'last_name']