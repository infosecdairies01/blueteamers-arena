from django.db import models
from apps.common.models.base import BaseModel
from apps.participants.models.participant import Participant
from apps.challenges.models.challenge import Challenge


class ParticipantProgress(BaseModel):
    """
    Tracks a student participant's progress status for a specific CTF challenge.
    """
    class StatusChoices(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="challenge_progresses")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="participant_progresses")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NOT_STARTED,
        db_index=True,
    )
    current_question_index = models.PositiveIntegerField(default=0)
    visited_questions = models.JSONField(default=list, blank=True)
    score_earned = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = "Participant Progress"
        verbose_name_plural = "Participant Progresses"
        unique_together = ["participant", "challenge"]
        ordering = ["challenge__challenge_number"]
        indexes = [
            models.Index(fields=["participant", "challenge"]),
            models.Index(fields=["participant", "status"]),
        ]

    def __str__(self):
        return f"{self.participant.name} - {self.challenge.slug} ({self.status})"
