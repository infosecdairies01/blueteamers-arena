from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base Model Serializer providing default read-only UUID and ISO timestamp fields.
    """
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")


class BaseResponseSerializer(serializers.Serializer):
    """
    Base Serializer for standard API JSON response structures.
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(default="Operation completed successfully.")
    data = serializers.SerializerMethodField(required=False)
    errors = serializers.SerializerMethodField(required=False)
