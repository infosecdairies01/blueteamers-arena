from typing import Optional
from django.db.models import QuerySet
from apps.submissions.models.submission import Submission


class SubmissionSelector:
    @staticmethod
    def get_by_id(submission_id: str) -> Optional[Submission]:
        try:
            return Submission.objects.get(id=submission_id)
        except (Submission.DoesNotExist, ValueError):
            return None

    @staticmethod
    def get_participant_submissions(participant_id: str, challenge_id: Optional[str] = None) -> QuerySet[Submission]:
        qs = Submission.objects.filter(participant_id=participant_id).select_related("challenge")
        if challenge_id:
            qs = qs.filter(challenge_id=challenge_id)
        return qs.order_by("-submitted_at")
