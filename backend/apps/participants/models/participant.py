from django.db import models
from apps.common.models.base import BaseModel
from apps.events.models.event import Event


class Participant(BaseModel):
    """
    Student Participant model representing student registration for a specific Event.
    Relationship: One Event -> Many Participants.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    name = models.CharField(max_length=150)
    email = models.EmailField(db_index=True)
    score = models.PositiveIntegerField(default=0, db_index=True)
    completed = models.PositiveIntegerField(default=0)  # Count of completed challenges
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        ordering = ["-score", "finished_at", "-created_at"]
        unique_together = ["event", "email"]
        indexes = [
            models.Index(fields=["event", "email"]),
            models.Index(fields=["event", "score"]),
            models.Index(fields=["score", "finished_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.event.event_code}"
