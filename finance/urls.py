from django.urls import path
from finance.views import finance_view, finance_create

urlpatterns = [
    path('money/', finance_view, name='money_list_view'),
    path('money/create/', finance_create, name='money_create_view'),
]