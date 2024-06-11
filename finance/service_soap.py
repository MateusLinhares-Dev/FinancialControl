from django.http import HttpResponse
from userFinance.models import UserFinance
from finance.models import FinanceView
from django.views.decorators.csrf import csrf_exempt
from lxml import etree

@csrf_exempt
def service_soap_balance(request):
    if request.method == "GET":
        balances = FinanceView.objects.all()

        envelope = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Envelope")
        body = etree.SubElement(envelope,"{http://schemas.xmlsoap.org/soap/envelope}body")
        response = etree.SubElement(body, "getBalanceFinancial", xlmns="http://example.com/soap/")

        for balance in balances:
            balance_element = etree.SubElement(response, "Balance")
            etree.SubElement(balance_element, "id").text = str(balance.id)
            etree.SubElement(balance_element, "balance").text = str(balance.valueInsert)
            etree.SubElement(balance_element, "user").text = str(balance.user)
            etree.SubElement(balance_element, "money").text = str(balance.money)
            etree.SubElement(balance_element, "description").text = str(balance.description)
            
        response_xml = etree.tostring(envelope, pretty_print=True, xml_declaration=True,encoding="UTF-8")
        return HttpResponse(response_xml, content_type='text/xml')



    
    
