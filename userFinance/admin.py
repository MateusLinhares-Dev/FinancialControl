from django.contrib import admin
from userFinance.models import UserFinance

@admin.register(UserFinance)
class FinanceUser(admin.ModelAdmin):
    list_display = ('id', 'name','birthday')
