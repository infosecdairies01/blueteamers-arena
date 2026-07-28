from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models.user import User
from apps.questions.models.question import Question


class QuestionsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="qadmin@blueteamers.io",
            password="AdminPassword123!",
            role=User.RoleChoices.ADMIN,
        )
        self.question = Question.objects.create(
            category=Question.CategoryChoices.PHISHING,
            difficulty=Question.DifficultyChoices.EASY,
            kind=Question.QuestionKindChoices.TEXT,
            question_text="What is the spoofed sender domain?",
            correct_answer="payroll-secure-verify.com",
            explanation="Return-Path shows envelope sender.",
            default_points=10,
        )
        self.list_url = reverse("question-list")
        self.detail_url = reverse("question-detail", kwargs={"pk": str(self.question.id)})

    def test_public_question_list_strips_answer_key(self):
        # Unauthenticated / Public student access
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = response.data["results"][0]
        
        self.assertIn("prompt", item)
        self.assertNotIn("correct_answer", item)
        self.assertNotIn("correct_option_index", item)
        self.assertNotIn("explanation", item)

    def test_admin_question_list_includes_answer_key(self):
        # Authenticated Admin access
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = response.data["results"][0]

        self.assertIn("correct_answer", item)
        self.assertIn("explanation", item)

    def test_create_question_admin(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "category": "SIEM",
            "difficulty": "Medium",
            "kind": "mcq",
            "question_text": "What level alert is critical in Wazuh?",
            "options_json": ["Level 3", "Level 7", "Level 12", "Level 15"],
            "correct_option_index": 3,
            "explanation": "Level 15 is critical.",
            "default_points": 15,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)
