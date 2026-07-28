from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from apps.accounts.permissions.is_admin import IsAdmin
from apps.audit.selectors.audit_selector import AuditSelector
from apps.audit.serializers.audit_serializer import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        action_type = self.request.query_params.get("action_type")
        search_query = self.request.query_params.get("search")
        return AuditSelector.filter_audit_logs(action_type=action_type, search_query=search_query)
