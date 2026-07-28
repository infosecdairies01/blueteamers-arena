from typing import Optional
from django.db import models
from django.db.models import QuerySet
from apps.events.models.event import Event


class EventSelector:
    @staticmethod
    def get_by_id(event_id: str) -> Optional[Event]:
        try:
            return Event.objects.get(id=event_id)
        except (Event.DoesNotExist, ValueError):
            return None

    @staticmethod
    def get_by_code(code: str) -> Optional[Event]:
        try:
            return Event.objects.get(event_code__iexact=code.strip())
        except Event.DoesNotExist:
            return None

    @staticmethod
    def filter_events(status: Optional[str] = None, query: Optional[str] = None) -> QuerySet[Event]:
        qs = Event.objects.all()
        if status and status != "All":
            qs = qs.filter(status=status)
        if query:
            q = query.strip()
            qs = qs.filter(
                models.Q(college_name__icontains=q) |
                models.Q(workshop_name__icontains=q) |
                models.Q(event_code__icontains=q)
            )
        return qs.order_by("-event_date", "-created_at")
