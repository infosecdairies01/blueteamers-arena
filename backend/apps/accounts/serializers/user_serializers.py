from rest_framework import serializers
from apps.accounts.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User Profile model details.
    """
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "email", "role", "is_active", "is_staff", "created_at", "updated_at"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating authenticated User profile info.
    """
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]
