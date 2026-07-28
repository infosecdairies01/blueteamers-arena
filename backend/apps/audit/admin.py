from django.contrib import admin
from apps.audit.models.audit_log import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action_type", "user", "description_short", "ip_address", "timestamp")
    list_filter = ("action_type", "timestamp")
    search_fields = ("description", "user__email", "ip_address")
    ordering = ("-timestamp",)

    def description_short(self, obj):
        return obj.description[:60]
    description_short.short_description = "Description"
