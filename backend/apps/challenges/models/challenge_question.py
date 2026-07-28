from django.db import models
from apps.common.models.base import BaseModel
from .challenge import Challenge
from apps.questions.models.question import Question


class ChallengeQuestion(BaseModel):
    """
    Junction model mapping Questions to CTF Challenges with sequence position.
    """
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="challenge_questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="assigned_challenges")
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Challenge Question"
        verbose_name_plural = "Challenge Questions"
        ordering = ["position", "created_at"]
        unique_together = ["challenge", "question"]
        indexes = [
            models.Index(fields=["challenge", "position"]),
        ]

    def __str__(self):
        return f"{self.challenge.slug} - Question #{self.position}"
