import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models.user import User


class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.super_admin = User.objects.create_superuser(
            email="superadmin@blueteamers.io",
            password="SuperPassword123!",
            first_name="Super",
            last_name="Admin",
        )
        self.admin = User.objects.create_user(
            email="admin@blueteamers.io",
            password="AdminPassword123!",
            first_name="Normal",
            last_name="Admin",
            role=User.RoleChoices.ADMIN,
        )
        self.me_url = reverse("auth-me")

    def test_user_uuid_primary_key(self):
        self.assertIsInstance(self.admin.id, uuid.UUID)

    def test_user_roles(self):
        self.assertTrue(self.super_admin.is_super_admin_role)
        self.assertTrue(self.super_admin.is_admin_role)

        self.assertTrue(self.admin.is_admin_role)
        self.assertFalse(self.admin.is_super_admin_role)

    def test_get_user_profile_me(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["email"], "admin@blueteamers.io")
        self.assertEqual(response.data["data"]["role"], "ADMIN")

    def test_update_user_profile_me(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            self.me_url,
            {"first_name": "UpdatedFirst", "phone_number": "+1234567890"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["first_name"], "UpdatedFirst")
        self.assertEqual(response.data["data"]["phone_number"], "+1234567890")
