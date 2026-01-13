from django.utils.deprecation import MiddlewareMixin


class Session_init(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.get('info'):
            request.session["info"] = {"id": None, "name": None, "depart": None}
