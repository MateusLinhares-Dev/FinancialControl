import base64
from django.contrib.auth import authenticate
from django.http import HttpResponse

class AuthCredentials:
   
    @staticmethod
    def is_authenticated(request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            auth_type, credentials = auth_header.split()
            if auth_type.lower() == 'basic':
                credentials = base64.b64decode(credentials).decode('utf-8')
                username, password = credentials.split(':')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    return user
        return None
