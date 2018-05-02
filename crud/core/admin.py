from django.contrib import admin
from .models import BankUser, BankAccount


# class BankUserAdmin(admin.ModelAdmin):
#     class Meta:
#         model = BankUser
#
#
# class BankAccountAdmin(admin.ModelAdmin):
#     class Meta:
#         model = BankAccount

class BankAccountInline(admin.TabularInline):
    model = BankAccount


class BankAccountAdmin(admin.ModelAdmin):
    inlines = [BankAccountInline]


admin.site.register(BankUser, BankAccountAdmin)
