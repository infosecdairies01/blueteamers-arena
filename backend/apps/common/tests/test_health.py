from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class HealthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.health_url = reverse("health-list")

    def test_health_check_endpoint(self):
        response = self.client.get(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["status"], "healthy")
        self.assertIn("database", response.data["data"]["components"])
        self.assertEqual(response.data["data"]["components"]["database"]["status"], "healthy")
