from django.urls import path
from finance.service_soap import service_soap_balance

urlpatterns = [
    path('balance/', service_soap_balance, name='money_list_view'),
]