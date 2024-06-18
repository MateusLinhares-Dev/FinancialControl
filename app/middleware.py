from app.is_authenticated import AuthCredentials
from django.http import HttpResponse

class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = AuthCredentials.is_authenticated(request)
        if user is None:
            return self.unauthorized_response()

        request.user = user
        return self.get_response(request)

    def unauthorized_response(self):
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic'
    
        return response
