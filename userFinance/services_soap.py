from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from userFinance.models import UserFinance
from django.views.decorators.csrf import csrf_exempt
from lxml import etree


@csrf_exempt
def user_soap_review_insert(request):
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
    
    if request.method == "POST":
        envelope = etree.fromstring(request.body)
        operation = envelope.find('.//{http://example.com/soap/}infoUser')

        if operation is not None:
            name = operation.find('name').text
            birthday = operation.find('birthday').text
            save_user = UserFinance(name=name, birthday=birthday)
            save_user.save()

            response = f"""
             <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Body>
                    <addUser xmlns="http://example.com/soap/">
                        <id>{save_user.id}</id>
                        <name>{name}</name>
                        <birthday>{birthday}</birthday>
                    </addUser>
                </soapenv:Body>
            </soapenv:Envelope>
            """
            return HttpResponse(response, content_type='text/xml')
    return HttpResponse("Invalid request method.", status=405)


@csrf_exempt
def user_soap_detail_update_delete(request):
    if request.method == 'POST':
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
        return HttpResponse("Invalid SOAP OPERATION.", status=405)
    
    if request.method == 'DELETE':
        envelope = etree.fromstring(request.body)
        operation = envelope.find('.//{http://user.com/soap/}Delete')

        if operation is not None:
            delete_id = operation.find('id').text

        try:
            user_view = UserFinance.objects.get(id=delete_id)

        except ObjectDoesNotExist:

            return HttpResponse("Invalid ID user, doesn't exist", status=404)

        try:
            user_view.delete()

            return HttpResponse("Record deleted successfully!", content_type="txt/xml")
        
        except ProtectedError:
                
                return HttpResponse("This user has records, delete them!", status=404)
        
    if request.method == 'PUT':
        envelope = etree.fromstring(request.body)
        operation = envelope.find(".//{http://user.com/soap/}update")

        try:
            user_finance = UserFinance.objects.get(id=operation[0].text)

        except ObjectDoesNotExist:

            return HttpResponse("Invalid ID user, doesn't exist", status=404)

        if operation is not None:

            for element in operation:
                tag = element.tag
                value_update = element.text

                if hasattr(user_finance, tag):
                    setattr(user_finance, tag, value_update)

            user_finance.save()

            response_xml = f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soapenv:Body>
                        <addUser xmlns="http://user.com/soap/">
                            <id>{user_finance.id}</id>
                            <user>{user_finance.name}</user>
                            <birthday>{user_finance.birthday}</birthday>
                        </addUser>
                    </soapenv:Body>
                </soapenv:Envelope>
                """ 
            return HttpResponse(response_xml, status=201, content_type="txt/xml")
        
    return HttpResponse("INVALID METHOD", status=404)


def wsdl_view(request):

    if request.method == 'GET':
        wsdl_content = open('userFinance/wsdl.xml').read()
        return HttpResponse(wsdl_content, content_type='text/xml')
    
    return HttpResponse("Invalid method", status=405)