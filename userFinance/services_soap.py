from django.http import HttpResponse
from userFinance.models import UserFinance
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
   
def soap_service_user(request):
    if request.method == "GET":
        users = UserFinance.objects.all()

        envelope = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Envelope")
        body = etree.SubElement(envelope, "{http://schemas.xmlsoap.org/soap/envelope/}Body")
        response = etree.SubElement(body, "getUsersResponse", xmlns="http://example.com/soap/")
        
        for user in users:
            user_element = etree.SubElement(response, "User")
            etree.SubElement(user_element, "id").text = str(user.id)
            etree.SubElement(user_element, "name").text = user.name
            etree.SubElement(user_element, "birthday").text = str(user.birthday)
        
        response_xml = etree.tostring(envelope, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        return HttpResponse(response_xml, content_type='text/xml')
    
    return HttpResponse("Invalid request method.", status=405)


@csrf_exempt
def soap_service_user_detail(request):
    if request.method == "POST":
        envelope = etree.fromstring(request.body)
        operation = envelope.find('.//{http://example.com/soap/}add')
        if operation is not None:
            id = operation.find('id').text
            user = UserFinance.objects.get(id=id)
            print(user)
            response = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Body>
                    <addUser xmlns="http://example.com/soap/">
                        <name>{user.name}</name>
                        <birthday>{user.birthday}</birthday>
                    </addUser>
                </soapenv:Body>
            </soapenv:Envelope>
            """
            return HttpResponse(response, content_type='text/xml')
        return HttpResponse("Invalid SOAP OPERATION.", status=400)
    return HttpResponse("Method invalid, required 'POST'. ", status=404)

        

def wsdl_view(request):
    wsdl_content = open('userFinance/wsdl.xml').read()
    return HttpResponse(wsdl_content, content_type='text/xml')