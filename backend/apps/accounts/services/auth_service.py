from typing import Dict, Any
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models.user import User


class AuthService:
    """
    Business Logic Service for Authentication operations (Login, Token Refresh, Logout).
    """

    @staticmethod
    def login_admin(email: str, password: str) -> Dict[str, Any]:
        user = authenticate(username=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid email or password.")
        
        if not user.is_active:
            raise AuthenticationFailed("This user account is inactive.")

        if not user.is_admin_role:
            raise AuthenticationFailed("Access denied. Admin permissions required.")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
        }

    @staticmethod
    def refresh_access_token(refresh_token_str: str) -> Dict[str, str]:
        try:
            refresh = RefreshToken(refresh_token_str)
            return {
                "access": str(refresh.access_token),
            }
        except Exception as e:
            raise ValidationError(f"Invalid or expired refresh token: {str(e)}")

    @staticmethod
    def logout(refresh_token_str: str) -> None:
        try:
            token = RefreshToken(refresh_token_str)
            token.blacklist()
        except Exception as e:
            raise ValidationError(f"Invalid refresh token or already blacklisted: {str(e)}")
