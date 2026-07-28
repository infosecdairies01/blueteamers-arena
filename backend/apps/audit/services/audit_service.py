from typing import Dict, Any, Optional
from apps.audit.models.audit_log import AuditLog
from apps.accounts.models.user import User


class AuditService:
    @staticmethod
    def log_action(
        user: Optional[User],
        action_type: str,
        description: str,
        ip_address: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        return AuditLog.objects.create(
            user=user if (user and user.is_authenticated) else None,
            action_type=action_type,
            description=description,
            ip_address=ip_address,
            payload=payload or {},
        )
