from django.http import JsonResponse
from django.conf import settings


class SuspiciousIPMiddleware:
    """
    Middleware for blocking suspicious or blacklisted IP addresses.
    """
    BLOCKED_IPS = getattr(settings, "BLOCKED_IPS", set())

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if ip in self.BLOCKED_IPS:
            return JsonResponse({
                "success": False,
                "message": "Access denied. Your IP address has been blocked due to security policy.",
            }, status=403)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip or ""
