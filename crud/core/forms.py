from django import forms
from .models import BankUser, BankAccount
from django.forms.models import BaseInlineFormSet


class BankUserForm(forms.ModelForm):
    class Meta:
        model = BankUser
        fields = ['first_name', 'last_name']

# class BankAccountForm(forms.ModelForm):
#     class Meta:
#         model = BankAccount
#         fields = ['IBAN']


# from django.forms.models import inlineformset_factory
#
#
# class BaseChildrenFormset(BaseInlineFormSet):
#     pass
#
# ChildrenFormset = inlineformset_factory(BankUser,
#                                         BankAccount,
#                                         formset=BaseChildrenFormset,
#                                         extra=1)