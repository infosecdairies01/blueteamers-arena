from django.db import models
from apps.common.models.base import BaseModel
from apps.participants.models.participant import Participant
from apps.challenges.models.challenge import Challenge
from apps.questions.models.question import Question


class ParticipantDraftAnswer(BaseModel):
    """
    Autosaves student draft answers per question without submitting/grading.
    """
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="draft_answers")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="participant_drafts")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="participant_drafts")
    answer_text = models.TextField(blank=True, default="")
    selected_options = models.JSONField(default=list, blank=True)
    selected_option_index = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Participant Draft Answer"
        verbose_name_plural = "Participant Draft Answers"
        unique_together = ["participant", "challenge", "question"]
        indexes = [
            models.Index(fields=["participant", "challenge"]),
        ]

    def __str__(self):
        return f"{self.participant.name} Draft - Q:{self.question_id}"
