from django.conf import settings
from django.http import HttpResponseForbidden

class IPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/raffles/') and request.method == 'POST' and 'winners' not in request.path:
            if request.META['REMOTE_ADDR'] not in settings.MANAGER_IPS:
                return HttpResponseForbidden("You are not allowed to access this endpoint.")
        response = self.get_response(request)
        return response
