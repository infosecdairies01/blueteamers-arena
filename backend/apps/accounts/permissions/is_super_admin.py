from rest_framework.permissions import BasePermission
from apps.accounts.models.user import User


class IsSuperAdmin(BasePermission):
    """
    Custom permission allowing access ONLY to SUPER_ADMIN users or is_superuser.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == User.RoleChoices.SUPER_ADMIN or request.user.is_superuser)
        )
