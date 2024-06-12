from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from userFinance.models import UserFinance
from finance.models import FinanceView
from django.views.decorators.csrf import csrf_exempt
from lxml import etree

#create e read
@csrf_exempt
def soap_detail_create(request):
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
    
    if request.method == "POST":
        envelope = etree.fromstring(request.body)
        operation = envelope.find('.//{http://balance.com/soap}Balance')

        if operation is not None:
            value_insert = operation.find('valueInsert').text
            user_id = operation.find('user').text
            money = operation.find('money').text
            description = operation.find('description').text

            try:
                user = UserFinance.objects.get(id=user_id)
            except ObjectDoesNotExist:
                return HttpResponse("Invalid ID user, doesn't exist", status=404)   
            
            financial_save = FinanceView(
                valueInsert=value_insert, 
                user=user, 
                money=money, 
                description=description)
            
            financial_save.save()
            
            response = f"""
             <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Body>
                    <addUser xmlns="http://example.com/soap/">
                        <id>{financial_save.id}</id>
                        <value_insert>{value_insert}</value_insert>
                        <user>{user}</user>
                        <money>{money}</money>
                        <description>{description}</description>
                    </addUser>
                </soapenv:Body>
            </soapenv:Envelope>
            """  

            return HttpResponse(response, status=201)
        return HttpResponse(f"Invalid method - {request.method}", status=404)


#Delete and update
@csrf_exempt
def soap_delete_update(request):
    if request.method == "DELETE":
        envelope = etree.fromstring(request.body)
        operation = envelope.find('.//{http://balance.com/soap}Delete')

        if operation is not None:
            delete_id = operation.find('id').text

        try:
            finance_view = FinanceView.objects.get(id=delete_id)
            finance_view.delete()
            
            return HttpResponse("Record deleted successfully!", content_type="txt/xml")
        
        except ObjectDoesNotExist:
            return HttpResponse("Invalid ID user, doesn't exist", status=404)   
    
    if request.method == "PUT":
        envelope = etree.fromstring(request.body)
        operation = envelope.find('.//{http://balance.com/soap}update')

        try:
            finance_view = FinanceView.objects.get(id=str(operation[0].text))
        except ObjectDoesNotExist:
            return HttpResponse("Invalid ID user, doesn't exist", status=404) 
        
        if operation is not None:
    
            for element in operation:
                tag = element.tag
                value_update = element.text
                
                if hasattr(finance_view, tag):
                    setattr(finance_view, tag, value_update)

            finance_view.save()    

            response_xml = f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soapenv:Body>
                        <addUser xmlns="http://example.com/soap/">
                            <id>{finance_view.id}</id>
                            <value_insert>{finance_view.valueInsert}</value_insert>
                            <user>{finance_view.user}</user>
                            <money>{finance_view.money}</money>
                            <description>{finance_view.description}</description>
                        </addUser>
                    </soapenv:Body>
                </soapenv:Envelope>
                """  
            

            return HttpResponse(response_xml, status=201, content_type="txt/xml")
    return HttpResponse("INVALID METHOD", status=404)