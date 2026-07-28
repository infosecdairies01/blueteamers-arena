from datetime import date
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.events.models.event import Event
from apps.participants.models.participant import Participant
from apps.participants.services.session_service import SessionService


class ParticipantAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = Event.objects.create(
            college_name="CBIT",
            workshop_name="AI with SOC Workshop",
            event_code="CBIT2026",
            event_date=date(2026, 7, 22),
            duration_minutes=60,
            status=Event.StatusChoices.LIVE,
        )
        self.participant = Participant.objects.create(
            event=self.event,
            name="Test Student",
            email="student@cbit.ac.in",
        )
        self.token = SessionService.generate_participant_token(self.participant)
        self.dashboard_url = reverse("student-dashboard-list")

    def test_authenticated_student_access(self):
        self.client.credentials(HTTP_X_PARTICIPANT_TOKEN=self.token)
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["student_profile"]["email"], "student@cbit.ac.in")

    def test_unauthenticated_student_access_rejected(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
