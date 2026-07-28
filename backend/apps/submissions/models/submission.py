from django.db import models
from apps.common.models.base import BaseModel
from apps.participants.models.participant import Participant
from apps.challenges.models.challenge import Challenge


class Submission(BaseModel):
    """
    Stores student challenge submission attempts and evaluation log outputs.
    """
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="submissions")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    answers_json = models.JSONField(default=dict)
    score_earned = models.PositiveIntegerField(default=0)
    max_possible_score = models.PositiveIntegerField(default=100)
    is_passing = models.BooleanField(default=False)
    evaluation_results = models.JSONField(default=list, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["participant", "challenge"]),
            models.Index(fields=["submitted_at"]),
        ]

    def __str__(self):
        return f"{self.participant.name} - {self.challenge.name} ({self.score_earned}/{self.max_possible_score})"
