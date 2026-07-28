from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models.user import User
from apps.accounts.models.password_reset import PasswordResetToken


class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email="admin@blueteamers.io",
            password="AdminPassword123!",
            first_name="Admin",
            last_name="User",
            role=User.RoleChoices.ADMIN,
        )
        self.login_url = reverse("auth-login")
        self.refresh_url = reverse("auth-token-refresh")
        self.logout_url = reverse("auth-logout")
        self.change_password_url = reverse("auth-change-password")
        self.forgot_password_url = reverse("auth-forgot-password")
        self.reset_password_url = reverse("auth-reset-password")

    def test_admin_login_success(self):
        response = self.client.post(
            self.login_url,
            {"email": "admin@blueteamers.io", "password": "AdminPassword123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["email"], "admin@blueteamers.io")

    def test_admin_login_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {"email": "admin@blueteamers.io", "password": "WrongPassword!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])

    def test_token_refresh(self):
        login_res = self.client.post(
            self.login_url,
            {"email": "admin@blueteamers.io", "password": "AdminPassword123!"},
            format="json",
        )
        refresh_token = login_res.data["data"]["refresh"]

        response = self.client.post(
            self.refresh_url,
            {"refresh": refresh_token},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["data"])

    def test_logout(self):
        login_res = self.client.post(
            self.login_url,
            {"email": "admin@blueteamers.io", "password": "AdminPassword123!"},
            format="json",
        )
        access_token = login_res.data["data"]["access"]
        refresh_token = login_res.data["data"]["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(
            self.logout_url,
            {"refresh": refresh_token},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        login_res = self.client.post(
            self.login_url,
            {"email": "admin@blueteamers.io", "password": "AdminPassword123!"},
            format="json",
        )
        access_token = login_res.data["data"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(
            self.change_password_url,
            {
                "old_password": "AdminPassword123!",
                "new_password": "NewSecretPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify login with new password
        new_login = self.client.post(
            self.login_url,
            {"email": "admin@blueteamers.io", "password": "NewSecretPassword123!"},
            format="json",
        )
        self.assertEqual(new_login.status_code, status.HTTP_200_OK)

    def test_forgot_and_reset_password_flow(self):
        # Trigger forgot password
        forgot_res = self.client.post(
            self.forgot_password_url,
            {"email": "admin@blueteamers.io"},
            format="json",
        )
        self.assertEqual(forgot_res.status_code, status.HTTP_200_OK)

        token_obj = PasswordResetToken.objects.get(user=self.admin_user, is_used=False)

        # Reset password
        reset_res = self.client.post(
            self.reset_password_url,
            {
                "token": token_obj.token,
                "new_password": "ResetPassword987!",
            },
            format="json",
        )
        self.assertEqual(reset_res.status_code, status.HTTP_200_OK)

        # Verify token marked used
        token_obj.refresh_from_db()
        self.assertTrue(token_obj.is_used)

        # Verify login with reset password
        login_res = self.client.post(
            self.login_url,
            {"email": "admin@blueteamers.io", "password": "ResetPassword987!"},
            format="json",
        )
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
