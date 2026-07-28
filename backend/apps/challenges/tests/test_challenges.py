from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.challenges.models.challenge import Challenge
from apps.challenges.models.evidence import Evidence


class ChallengesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.challenge = Challenge.objects.create(
            challenge_number=1,
            slug="phishnet",
            name="Operation PhishNet",
            description="Phishing investigation scenario",
            brief="Analyze suspicious email headers",
            difficulty=Challenge.DifficultyChoices.EASY,
            duration_minutes=20,
            points=100,
        )
        self.evidence = Evidence.objects.create(
            challenge=self.challenge,
            artifact_key="headers",
            label="Email Headers",
            filename="email-headers.txt",
            file_format=Evidence.FormatChoices.TXT,
            content_text="Return-Path: <spoofed@domain.com>",
        )
        self.list_url = reverse("challenge-list")
        self.detail_url = reverse("challenge-detail", kwargs={"slug": "phishnet"})

    def test_list_challenges(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Operation PhishNet")

    def test_get_challenge_detail_with_evidence(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], "phishnet")
        self.assertEqual(len(response.data["evidence"]), 1)
        self.assertEqual(response.data["evidence"][0]["artifact_key"], "headers")
