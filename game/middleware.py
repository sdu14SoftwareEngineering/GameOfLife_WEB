from django.http import HttpResponseRedirect


class UserMiddleware:
    def process_request(self, request):
        if request.path != '/login/':
            if 'username' in request.COOKIES:
                pass
            else:
                return HttpResponseRedirect('xxxxxxx')
