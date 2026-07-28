from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return self.cache_format % {"scope": self.scope, "ident": request.user.id}
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class VerifyCodeRateThrottle(SimpleRateThrottle):
    scope = "verify_code"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}
