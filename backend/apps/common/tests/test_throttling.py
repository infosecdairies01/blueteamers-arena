from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class RateLimitingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("auth-login")

    def test_login_throttling_structure(self):
        # Verify endpoint works under normal rate
        response = self.client.post(
            self.login_url,
            {"email": "nonexistent@test.com", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
