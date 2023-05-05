from user.models import UserLog


class LogMiddleware:

    def log_middleware(self, request_method, url):

        try:
            logs = UserLog.objects.get(request_method=request_method, url=url)
            logs.count += 1
            logs.save()

        except:
            UserLog.objects.create(request_method=request_method, url=url)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before view
        response = self.get_response(request)
        # after view
        self.log_middleware(request.method, request.path)
        return response
