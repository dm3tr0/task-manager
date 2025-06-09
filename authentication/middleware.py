
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        response = self.get_response(request)


        response.headers['X-MY-HEADER'] = '1111'

        return response