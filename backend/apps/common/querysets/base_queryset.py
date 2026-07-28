from django.db import models


class BaseQuerySet(models.QuerySet):
    """
    Base Custom QuerySet providing reusable active/recent filtering methods.
    """
    def active(self):
        if hasattr(self.model, "is_active"):
            return self.filter(is_active=True)
        return self

    def recent(self):
        if hasattr(self.model, "created_at"):
            return self.order_by("-created_at")
        return self
