import os
from datetime import datetime
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from apps.common.utils.response import success_response, error_response


class HealthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(responses={200: dict, 503: dict})
    def list(self, request):
        components = {}
        is_healthy = True

        # 1. Database Check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
            components["database"] = {
                "status": "healthy",
                "engine": connection.vendor,
            }
        except Exception as e:
            is_healthy = False
            components["database"] = {
                "status": "unhealthy",
                "error": str(e),
            }

        # 2. Cache / Redis Check
        try:
            cache.set("health_check_key", "ok", timeout=10)
            val = cache.get("health_check_key")
            if val == "ok":
                components["cache"] = {
                    "status": "healthy",
                    "backend": "redis/memory",
                }
            else:
                is_healthy = False
                components["cache"] = {
                    "status": "unhealthy",
                    "error": "Cache write read verification failed",
                }
        except Exception as e:
            # Cache failure is degraded but non-fatal for basic health if configured
            components["cache"] = {
                "status": "degraded",
                "error": str(e),
            }

        # 3. Storage Check
        try:
            media_root = getattr(settings, "MEDIA_ROOT", None) or os.getcwd()
            writable = os.access(media_root, os.W_OK)
            components["storage"] = {
                "status": "healthy" if writable else "unhealthy",
                "writable": writable,
            }
        except Exception as e:
            components["storage"] = {
                "status": "degraded",
                "error": str(e),
            }

        payload = {
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "components": components,
        }

        if is_healthy:
            return success_response(data=payload, message="Application health check passed.")
        else:
            return error_response(message="Application health check failed.", errors=payload, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
