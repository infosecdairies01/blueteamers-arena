import random
from typing import Dict, Any
from rest_framework.exceptions import ValidationError, NotFound
from apps.events.models.event import Event
from apps.events.selectors.event_selector import EventSelector


class EventService:
    @staticmethod
    def generate_event_code(college_name: str) -> str:
        base = "".join(c for c in college_name.upper() if c.isalnum())[:6] or "EVENT"
        rand = random.randint(1000, 9999)
        code = f"{base}-{rand}"
        while Event.objects.filter(event_code=code).exists():
            rand = random.randint(1000, 9999)
            code = f"{base}-{rand}"
        return code

    @staticmethod
    def create_event(data: Dict[str, Any], user=None) -> Event:
        code = data.get("event_code")
        college = data.get("college_name", "")
        if not code:
            code = EventService.generate_event_code(college)
        elif Event.objects.filter(event_code__iexact=code.strip()).exists():
            raise ValidationError({"event_code": ["An event with this code already exists."]})

        event = Event.objects.create(
            college_name=college,
            workshop_name=data.get("workshop_name", ""),
            event_code=code.upper(),
            event_date=data.get("event_date"),
            duration_minutes=data.get("duration_minutes", 60),
            passing_score=data.get("passing_score", 600),
            total_challenges=data.get("total_challenges", 5),
            accent_color=data.get("accent_color", "blue"),
            status=data.get("status", Event.StatusChoices.UPCOMING),
            created_by=user,
        )
        return event

    @staticmethod
    def verify_event_code(code: str) -> Event:
        event = EventSelector.get_by_code(code)
        if not event:
            raise NotFound("Invalid event code. Please check and try again.")
        return event
