from django.db import models
from apps.common.models.base import BaseModel
from apps.accounts.models.user import User


class AuditLog(BaseModel):
    """
    Security Audit Log for tracking all administrative and system operations.
    """
    class ActionType(models.TextChoices):
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        QUESTION_CREATE = "QUESTION_CREATE", "Question Create"
        QUESTION_UPDATE = "QUESTION_UPDATE", "Question Update"
        EVENT_UPDATE = "EVENT_UPDATE", "Event Update"
        PARTICIPANT_ACTION = "PARTICIPANT_ACTION", "Participant Action"
        ADMIN_ACTION = "ADMIN_ACTION", "Admin Action"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action_type = models.CharField(max_length=50, choices=ActionType.choices, db_index=True)
    description = models.TextField()
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    payload = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["action_type"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        user_str = self.user.email if self.user else "System"
        return f"[{self.action_type}] {user_str}: {self.description[:50]}"
