from typing import Dict, Any
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound
from apps.events.models.event import Event
from apps.participants.models.participant import Participant


class ParticipantService:
    @staticmethod
    def register_participant(event: Event, name: str, email: str) -> Participant:
        name = name.strip()
        email = email.strip().lower()

        if not name:
            raise ValidationError({"name": ["Student name is required."]})
        if not email:
            raise ValidationError({"email": ["College email ID is required."]})

        participant, created = Participant.objects.get_or_create(
            event=event,
            email=email,
            defaults={
                "name": name,
                "started_at": timezone.now(),
            },
        )
        if not created and not participant.started_at:
            participant.started_at = timezone.now()
            participant.save()

        return participant
