from django.urls import path
from .views import list_users, add_user, add_bank_account, delete_bank_account, update_user, delete_user


urlpatterns = [
    path('', list_users, name='home'),
    path('user', add_user, name='add_user'),
    path('user/<int:id>/add_bank_account', add_bank_account, name='add_bank_account'),
    path('user/delete_bank_account/<int:id>', delete_bank_account, name='delete_bank_account'),
    path('update/<int:id>', update_user, name='update_user'),
    path('delete/<int:id>', delete_user, name='delete_user'),
]
