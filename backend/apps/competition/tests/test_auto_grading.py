from django.test import TestCase
from apps.questions.models.question import Question
from apps.challenges.models.challenge import Challenge
from apps.challenges.models.challenge_question import ChallengeQuestion
from apps.competition.services.answer_validation_service import AnswerValidationService
from apps.competition.services.auto_grading_service import AutoGradingService


class AutoGradingEngineTests(TestCase):
    def setUp(self):
        self.q_text = Question.objects.create(
            category=Question.CategoryChoices.PHISHING,
            difficulty=Question.DifficultyChoices.EASY,
            kind=Question.QuestionKindChoices.TEXT,
            question_text="What is the spoofed domain?",
            correct_answer="payroll-secure-verify.com",
            default_points=10,
        )
        self.q_mcq = Question.objects.create(
            category=Question.CategoryChoices.SIEM,
            difficulty=Question.DifficultyChoices.MEDIUM,
            kind=Question.QuestionKindChoices.MCQ,
            question_text="What level alert is critical in Wazuh?",
            options_json=["Level 3", "Level 7", "Level 12", "Level 15"],
            correct_option_index=3,
            correct_answer="Level 15",
            default_points=20,
        )

        self.challenge = Challenge.objects.create(
            challenge_number=1,
            slug="phishnet",
            name="Operation PhishNet",
            description="Phishing scenario",
            brief="Analyze suspicious email headers",
            difficulty=Challenge.DifficultyChoices.EASY,
            duration_minutes=20,
            points=30,
        )
        ChallengeQuestion.objects.create(challenge=self.challenge, question=self.q_text, position=1)
        ChallengeQuestion.objects.create(challenge=self.challenge, question=self.q_mcq, position=2)

    def test_text_answer_validation_case_and_whitespace_insensitive(self):
        is_corr, score, _ = AnswerValidationService.validate_answer(self.q_text, "  PAYROLL-SECURE-VERIFY.COM  ")
        self.assertTrue(is_corr)
        self.assertEqual(score, 1.0)

    def test_mcq_answer_validation(self):
        is_corr_idx, score1, _ = AnswerValidationService.validate_answer(self.q_mcq, 3)
        self.assertTrue(is_corr_idx)
        self.assertEqual(score1, 1.0)

        is_corr_str, score2, _ = AnswerValidationService.validate_answer(self.q_mcq, "Level 15")
        self.assertTrue(is_corr_str)
        self.assertEqual(score2, 1.0)

    def test_full_challenge_auto_grading(self):
        submitted = {
            str(self.q_text.id): "payroll-secure-verify.com",
            str(self.q_mcq.id): 3,
        }
        result = AutoGradingService.grade_submission(self.challenge, submitted)
        self.assertEqual(result["score_earned"], 30)
        self.assertEqual(result["max_possible_score"], 30)
        self.assertTrue(result["is_passing"])
        self.assertEqual(len(result["evaluation_logs"]), 2)
