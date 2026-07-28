from django.db import models
from apps.common.models.base import BaseModel
from .event import Event


class EventQuestion(BaseModel):
    """
    Junction model mapping Questions assigned to a specific Event with sequence position.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_questions")
    question_id = models.UUIDField(db_index=True)  # References Question.id
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Event Question"
        verbose_name_plural = "Event Questions"
        ordering = ["position", "created_at"]
        unique_together = ["event", "question_id"]
        indexes = [
            models.Index(fields=["event", "position"]),
        ]

    def __str__(self):
        return f"{self.event.event_code} - Question #{self.position}"
