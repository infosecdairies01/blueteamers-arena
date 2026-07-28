from typing import Optional
from django.db import models
from django.db.models import QuerySet
from apps.questions.models.question import Question


class QuestionSelector:
    @staticmethod
    def get_by_id(question_id: str) -> Optional[Question]:
        try:
            return Question.objects.get(id=question_id)
        except (Question.DoesNotExist, ValueError):
            return None

    @staticmethod
    def filter_questions(
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
    ) -> QuerySet[Question]:
        qs = Question.objects.all()
        if category and category != "All":
            qs = qs.filter(category=category)
        if difficulty and difficulty != "All":
            qs = qs.filter(difficulty=difficulty)
        if status and status != "All":
            qs = qs.filter(status=status)
        if query:
            q = query.strip()
            qs = qs.filter(
                models.Q(question_text__icontains=q) |
                models.Q(evidence_text__icontains=q)
            )
        return qs.order_by("-created_at")
