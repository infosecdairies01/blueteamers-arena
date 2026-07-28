from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserValidator:
    """
    Validator service for User registration, password changes, and account inputs.
    """

    @staticmethod
    def validate_password_strength(password: str, user=None) -> None:
        validate_password(password, user=user)

    @staticmethod
    def validate_email_unique(email: str) -> None:
        from apps.accounts.models.user import User
        if User.objects.filter(email__iexact=email.strip()).exists():
            raise ValidationError("A user with this email address already exists.")
