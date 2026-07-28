from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models.user import User
from apps.audit.models.audit_log import AuditLog
from apps.audit.services.audit_service import AuditService


class AuditLogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="auditadmin@blueteamers.io",
            password="AdminPassword123!",
            role=User.RoleChoices.ADMIN,
        )
        self.log = AuditService.log_action(
            user=self.admin,
            action_type=AuditLog.ActionType.EVENT_UPDATE,
            description="Updated event CBIT2026 status to Live.",
            ip_address="127.0.0.1",
        )
        self.list_url = reverse("audit-log-list")

    def test_audit_log_creation(self):
        self.assertEqual(AuditLog.objects.count(), 1)
        self.assertEqual(self.log.action_type, "EVENT_UPDATE")

    def test_admin_list_audit_logs(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action_type"], "EVENT_UPDATE")
