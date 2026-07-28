import re
from typing import Dict, Any, Tuple
from apps.questions.models.question import Question


class AnswerValidationService:
    """
    Validation engine for comparing student answers against Question ground truth keys.
    Supports case-insensitive string matching, whitespace trimming, regex pattern evaluation,
    keyword substring checking, and MCQ exact index matching.
    """
    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
        return text.strip().lower()

    @classmethod
    def validate_answer(cls, question: Question, student_answer: Any) -> Tuple[bool, float, str]:
        """
        Validates student answer against question configuration.
        Returns Tuple[is_correct: bool, score_multiplier: float, feedback_note: str]
        """
        if question.kind == Question.QuestionKindChoices.MCQ:
            return cls._validate_mcq(question, student_answer)
        else:
            return cls._validate_text(question, student_answer)

    @classmethod
    def _validate_mcq(cls, question: Question, student_answer: Any) -> Tuple[bool, float, str]:
        target_idx = question.correct_option_index
        target_str = cls.normalize(question.correct_answer)

        # Check if student passed an integer index or index string
        if isinstance(student_answer, int) or (isinstance(student_answer, str) and student_answer.isdigit()):
            selected_idx = int(student_answer)
            if target_idx is not None and selected_idx == target_idx:
                return True, 1.0, "Correct MCQ selection!"
            return False, 0.0, "Incorrect MCQ selection."

        # Check if student passed the option string
        provided_str = cls.normalize(str(student_answer))
        if target_str and provided_str == target_str:
            return True, 1.0, "Correct MCQ selection!"

        # Check in options_json if target_idx is valid
        if target_idx is not None and 0 <= target_idx < len(question.options_json):
            expected_option_str = cls.normalize(str(question.options_json[target_idx]))
            if provided_str == expected_option_str:
                return True, 1.0, "Correct MCQ selection!"

        return False, 0.0, "Incorrect MCQ selection."

    @classmethod
    def _validate_text(cls, question: Question, student_answer: Any) -> Tuple[bool, float, str]:
        provided = cls.normalize(str(student_answer or ""))
        target = cls.normalize(question.correct_answer)

        if not provided:
            return False, 0.0, "No answer provided."

        # 1. Direct exact match (case-insensitive & trimmed)
        if provided == target:
            return True, 1.0, "Exact match!"

        # 2. Regex matching (if target contains regex meta characters like ^, $, .*, |)
        if any(char in target for char in ["^", "$", ".*", "|", "[", "]"]):
            try:
                if re.search(target, provided, re.IGNORECASE):
                    return True, 1.0, "Matched regex pattern!"
            except re.error:
                pass

        # 3. Substring keyword check (if target is a comma-separated list of keywords)
        keywords = [k.strip() for k in target.split(",") if k.strip()]
        if len(keywords) > 1:
            matched = [k for k in keywords if k in provided]
            if len(matched) == len(keywords):
                return True, 1.0, "Matched all required keywords!"
            elif len(matched) > 0:
                credit = round(len(matched) / len(keywords), 2)
                return True, credit, f"Partial match ({len(matched)}/{len(keywords)} keywords matched)."

        return False, 0.0, "Incorrect answer."
