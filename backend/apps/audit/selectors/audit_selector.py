from typing import Optional
from django.db.models import QuerySet
from apps.audit.models.audit_log import AuditLog


class AuditSelector:
    @staticmethod
    def filter_audit_logs(action_type: Optional[str] = None, search_query: Optional[str] = None) -> QuerySet[AuditLog]:
        qs = AuditLog.objects.all().select_related("user")
        if action_type and action_type != "All":
            qs = qs.filter(action_type=action_type)
        if search_query:
            q = search_query.strip()
            qs = qs.filter(description__icontains=q)
        return qs.order_by("-timestamp")
