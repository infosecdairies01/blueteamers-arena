from rest_framework.routers import DefaultRouter
from apps.audit.viewsets.audit_viewset import AuditLogViewSet

router = DefaultRouter()
router.register(r"audit-logs", AuditLogViewSet, basename="audit-log")

urlpatterns = router.urls
