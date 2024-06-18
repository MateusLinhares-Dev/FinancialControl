from django.urls import path
from userFinance.services_soap import user_soap_review_insert, wsdl_view, user_soap_detail_update_delete

urlpatterns= [
    path('soap/users/', user_soap_review_insert ),
    path('soap/users/detail/', user_soap_detail_update_delete),
    path('soap/users/wsdl/', wsdl_view)
]