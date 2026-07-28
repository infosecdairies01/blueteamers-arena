from typing import Dict, Any, List
from apps.challenges.models.challenge import Challenge
from apps.questions.models.question import Question
from apps.competition.services.answer_validation_service import AnswerValidationService


class AutoGradingService:
    """
    Auto-Grading Engine for evaluating student challenge submissions.
    """
    @staticmethod
    def grade_submission(challenge: Challenge, submitted_answers: Dict[str, Any]) -> Dict[str, Any]:
        challenge_questions = challenge.challenge_questions.select_related("question").order_by("position")

        total_score_earned = 0
        max_possible_score = 0
        evaluation_logs = []

        for cq in challenge_questions:
            q = cq.question
            max_possible_score += q.default_points

            student_ans = submitted_answers.get(str(q.id))
            if student_ans is None:
                # Try lookup by position or index
                student_ans = submitted_answers.get(f"q{cq.position}")

            is_correct, score_multiplier, note = AnswerValidationService.validate_answer(q, student_ans)
            points_earned = int(q.default_points * score_multiplier)
            total_score_earned += points_earned

            evaluation_logs.append({
                "question_id": str(q.id),
                "position": cq.position,
                "category": q.category,
                "default_points": q.default_points,
                "points_earned": points_earned,
                "is_correct": is_correct,
                "score_multiplier": score_multiplier,
                "feedback_note": note,
            })

        passing_threshold = int(max_possible_score * 0.6)  # 60% passing threshold
        is_passing = total_score_earned >= passing_threshold

        return {
            "score_earned": total_score_earned,
            "max_possible_score": max_possible_score,
            "is_passing": is_passing,
            "evaluation_logs": evaluation_logs,
        }
