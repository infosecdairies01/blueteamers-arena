from typing import Dict, Any, List
from django.utils import timezone
from rest_framework.exceptions import NotFound, ValidationError
from apps.participants.models.participant import Participant
from apps.participants.models.participant_progress import ParticipantProgress
from apps.participants.models.participant_draft import ParticipantDraftAnswer
from apps.challenges.models.challenge import Challenge
from apps.questions.models.question import Question


class ProgressService:
    @staticmethod
    def get_challenge_progress(participant: Participant, challenge: Challenge) -> Dict[str, Any]:
        progress, _ = ParticipantProgress.objects.get_or_create(
            participant=participant,
            challenge=challenge,
            defaults={"status": ParticipantProgress.StatusChoices.IN_PROGRESS, "started_at": timezone.now()},
        )

        drafts = ParticipantDraftAnswer.objects.filter(participant=participant, challenge=challenge)
        drafts_data = {}
        for d in drafts:
            drafts_data[str(d.question_id)] = {
                "answer_text": d.answer_text,
                "selected_options": d.selected_options,
                "selected_option_index": d.selected_option_index,
            }

        return {
            "challenge_slug": challenge.slug,
            "status": progress.status,
            "current_question_index": progress.current_question_index,
            "visited_questions": progress.visited_questions,
            "score_earned": progress.score_earned,
            "draft_answers": drafts_data,
            "started_at": progress.started_at.isoformat() if progress.started_at else None,
            "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
        }

    @staticmethod
    def save_draft(
        participant: Participant,
        challenge: Challenge,
        question_id: str,
        answer_text: str = "",
        selected_options: List[str] = None,
        selected_option_index: int = None,
        current_question_index: int = 0,
    ) -> Dict[str, Any]:
        try:
            question = Question.objects.get(id=question_id)
        except (Question.DoesNotExist, ValueError):
            raise NotFound("Question not found.")

        # Update or create draft answer
        ParticipantDraftAnswer.objects.update_or_create(
            participant=participant,
            challenge=challenge,
            question=question,
            defaults={
                "answer_text": answer_text,
                "selected_options": selected_options or [],
                "selected_option_index": selected_option_index,
            },
        )

        # Update progress state
        progress, _ = ParticipantProgress.objects.get_or_create(
            participant=participant,
            challenge=challenge,
            defaults={"started_at": timezone.now()},
        )
        if progress.status == ParticipantProgress.StatusChoices.NOT_STARTED:
            progress.status = ParticipantProgress.StatusChoices.IN_PROGRESS
            progress.started_at = timezone.now()

        progress.current_question_index = current_question_index
        visited = set(progress.visited_questions or [])
        visited.add(str(question.id))
        progress.visited_questions = list(visited)
        progress.save()

        return ProgressService.get_challenge_progress(participant, challenge)

    @staticmethod
    def submit_challenge(participant: Participant, challenge: Challenge) -> Dict[str, Any]:
        progress, _ = ParticipantProgress.objects.get_or_create(
            participant=participant,
            challenge=challenge,
        )

        if progress.status != ParticipantProgress.StatusChoices.COMPLETED:
            progress.status = ParticipantProgress.StatusChoices.COMPLETED
            progress.completed_at = timezone.now()
            progress.score_earned = challenge.points
            progress.save()

            # Update participant aggregate score & completed count
            participant.score += challenge.points
            participant.completed += 1
            if not participant.finished_at and participant.completed >= 5:
                participant.finished_at = timezone.now()
            participant.save()

        return {
            "message": f"Challenge '{challenge.name}' submitted successfully!",
            "challenge_slug": challenge.slug,
            "status": progress.status,
            "score_earned": progress.score_earned,
            "total_participant_score": participant.score,
            "completed_challenges": participant.completed,
        }
