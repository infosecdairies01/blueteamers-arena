from rest_framework import serializers
from apps.audit.models.audit_log import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True, default="System")

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user_email",
            "action_type",
            "description",
            "ip_address",
            "payload",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp"]
