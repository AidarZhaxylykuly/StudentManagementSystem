from analytics.models import APIUsageLog


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            APIUsageLog.objects.create(
                user=request.user,
                endpoint=request.path,
                method=request.method,
            )
        return self.get_response(request)