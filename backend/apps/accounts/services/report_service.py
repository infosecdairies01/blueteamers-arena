import csv
import json
import io
from typing import Dict, Any, List
from apps.participants.models.participant import Participant
from apps.questions.models.question import Question


class ReportService:
    @staticmethod
    def export_participants_csv(event_id: str = None) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Participant ID", "Name", "Email", "College Name", "Event Code", "Score", "Completed Challenges", "Started At", "Finished At"])

        qs = Participant.objects.all().select_related("event")
        if event_id:
            qs = qs.filter(event_id=event_id)

        for p in qs.order_by("-score", "finished_at"):
            writer.writerow([
                str(p.id),
                p.name,
                p.email,
                p.event.college_name,
                p.event.event_code,
                p.score,
                p.completed,
                p.started_at.isoformat() if p.started_at else "",
                p.finished_at.isoformat() if p.finished_at else "",
            ])

        return output.getvalue()

    @staticmethod
    def export_questions_json() -> List[Dict[str, Any]]:
        questions = Question.objects.all()
        data = []
        for q in questions:
            data.append({
                "category": q.category,
                "difficulty": q.difficulty,
                "kind": q.kind,
                "question_text": q.question_text,
                "evidence_text": q.evidence_text,
                "options_json": q.options_json,
                "correct_answer": q.correct_answer,
                "correct_option_index": q.correct_option_index,
                "explanation": q.explanation,
                "default_points": q.default_points,
                "status": q.status,
            })
        return data

    @staticmethod
    def import_questions_json(questions_data: List[Dict[str, Any]]) -> int:
        created_count = 0
        for item in questions_data:
            Question.objects.create(
                category=item.get("category", Question.CategoryChoices.PHISHING),
                difficulty=item.get("difficulty", Question.DifficultyChoices.EASY),
                kind=item.get("kind", Question.QuestionKindChoices.TEXT),
                question_text=item.get("question_text", ""),
                evidence_text=item.get("evidence_text", ""),
                options_json=item.get("options_json", []),
                correct_answer=item.get("correct_answer", ""),
                correct_option_index=item.get("correct_option_index", 0),
                explanation=item.get("explanation", ""),
                default_points=item.get("default_points", 10),
                status=item.get("status", Question.StatusChoices.PUBLISHED),
            )
            created_count += 1
        return created_count
