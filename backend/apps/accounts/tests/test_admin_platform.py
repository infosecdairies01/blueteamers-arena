from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models.user import User
from apps.events.models.event import Event
from apps.participants.models.participant import Participant


class AdminPlatformAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="platformadmin@blueteamers.io",
            password="AdminPassword123!",
            role=User.RoleChoices.ADMIN,
        )
        self.dashboard_url = reverse("admin-platform-dashboard")
        self.event_analytics_url = reverse("admin-platform-event-analytics")
        self.export_report_url = reverse("admin-platform-export-reports")

    def test_admin_dashboard_stats(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("summary", response.data["data"])
        self.assertIn("total_events", response.data["data"]["summary"])

    def test_export_participants_csv_report(self):
        self.client.force_authenticate(user=self.admin)
        payload = {"format": "csv"}
        response = self.client.post(self.export_report_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("Participant ID", response.content.decode("utf-8"))
