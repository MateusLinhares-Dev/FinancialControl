from django.contrib import admin
from finance.models import FinanceView

@admin.register(FinanceView)
class FinanceMoney(admin.ModelAdmin):
    list_display = ('id','user','money','description')