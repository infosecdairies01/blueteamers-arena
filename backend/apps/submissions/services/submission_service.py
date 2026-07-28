from typing import Dict, Any
from django.utils import timezone
from rest_framework.exceptions import ValidationError, PermissionDenied
from apps.participants.models.participant import Participant
from apps.participants.models.participant_progress import ParticipantProgress
from apps.challenges.models.challenge import Challenge
from apps.submissions.models.submission import Submission
from apps.competition.services.auto_grading_service import AutoGradingService
from apps.competition.services.websocket_service import WebSocketService


class SubmissionService:
    @staticmethod
    def submit_answers(participant: Participant, challenge: Challenge, answers: Dict[str, Any]) -> Submission:
        # Validate event is live
        if participant.event.status != "Live":
            raise PermissionDenied("Cannot submit answers for an event that is not Live.")

        # Grade submission via AutoGradingService
        grading_result = AutoGradingService.grade_submission(challenge, answers)

        # Save submission record
        submission = Submission.objects.create(
            participant=participant,
            challenge=challenge,
            answers_json=answers,
            score_earned=grading_result["score_earned"],
            max_possible_score=grading_result["max_possible_score"],
            is_passing=grading_result["is_passing"],
            evaluation_results=grading_result["evaluation_logs"],
        )

        # Update or create progress
        progress, _ = ParticipantProgress.objects.get_or_create(
            participant=participant,
            challenge=challenge,
        )
        if progress.status != ParticipantProgress.StatusChoices.COMPLETED:
            progress.status = ParticipantProgress.StatusChoices.COMPLETED
            progress.completed_at = timezone.now()
            progress.score_earned = grading_result["score_earned"]
            progress.save()

            # Update participant aggregate score
            participant.score += grading_result["score_earned"]
            participant.completed += 1
            if not participant.finished_at and participant.completed >= participant.event.total_challenges:
                participant.finished_at = timezone.now()
            participant.save()

        # WebSocket real-time broadcast
        event_code = participant.event.event_code
        WebSocketService.notify_submission_event(event_code, {
            "participant_name": participant.name,
            "challenge": challenge.name,
            "score_earned": grading_result["score_earned"],
            "total_score": participant.score,
        })

        return submission
