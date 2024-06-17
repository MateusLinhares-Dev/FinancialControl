from django.urls import path
from finance.service_soap import soap_detail_create, soap_delete_update, soap_wsdl_get

urlpatterns = [
    path('balance/', soap_detail_create, name='money_list_create_view'),
    path('financial/edit/', soap_delete_update, name='money_delete_update_view'),
    path('financial/wsdl', soap_wsdl_get, name='money_wsdl_get')
]