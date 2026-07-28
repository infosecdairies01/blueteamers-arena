from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from apps.common.utils.response import success_response, error_response
from apps.accounts.serializers.auth_serializers import (
    LoginSerializer,
    TokenRefreshSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from apps.accounts.services.auth_service import AuthService
from apps.accounts.services.password_service import PasswordService


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: LoginSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = AuthService.login_admin(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return success_response(data=data, message="Login successful.")


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=TokenRefreshSerializer)
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = AuthService.refresh_access_token(
            refresh_token_str=serializer.validated_data["refresh"]
        )
        return success_response(data=data, message="Token refreshed successfully.")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=LogoutSerializer)
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AuthService.logout(refresh_token_str=serializer.validated_data["refresh"])
        return success_response(message="Logout successful.")


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PasswordService.change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )
        return success_response(message="Password changed successfully.")


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msg = PasswordService.forgot_password(email=serializer.validated_data["email"])
        return success_response(message=msg)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PasswordService.reset_password(
            token_str=serializer.validated_data["token"],
            new_password=serializer.validated_data["new_password"],
        )
        return success_response(message="Password has been reset successfully.")
