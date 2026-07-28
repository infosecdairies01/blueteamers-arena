from typing import Optional
from django.db import models
from django.db.models import QuerySet
from apps.participants.models.participant import Participant


class ParticipantSelector:
    @staticmethod
    def get_by_id(participant_id: str) -> Optional[Participant]:
        try:
            return Participant.objects.get(id=participant_id)
        except (Participant.DoesNotExist, ValueError):
            return None

    @staticmethod
    def get_by_event_and_email(event_id: str, email: str) -> Optional[Participant]:
        try:
            return Participant.objects.get(event_id=event_id, email__iexact=email.strip())
        except Participant.DoesNotExist:
            return None

    @staticmethod
    def filter_participants(event_id: Optional[str] = None, query: Optional[str] = None) -> QuerySet[Participant]:
        qs = Participant.objects.all().select_related("event")
        if event_id:
            qs = qs.filter(event_id=event_id)
        if query:
            q = query.strip()
            qs = qs.filter(
                models.Q(name__icontains=q) |
                models.Q(email__icontains=q)
            )
        return qs.order_by("-score", "finished_at", "-created_at")
