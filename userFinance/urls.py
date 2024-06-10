from django.urls import path
from userFinance.services_soap import soap_service_user, wsdl_view, soap_service_user_detail

urlpatterns= [
    path('soap/users/', soap_service_user ),
    path('soap/users/detail/', soap_service_user_detail),
    path('soap/userswsdl/', wsdl_view)
]