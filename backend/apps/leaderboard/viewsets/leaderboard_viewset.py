from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from apps.common.utils.response import success_response
from apps.participants.auth.participant_auth import ParticipantTokenAuthentication
from apps.leaderboard.services.leaderboard_service import LeaderboardService
from apps.leaderboard.serializers.leaderboard_serializer import LeaderboardResponseSerializer


class LeaderboardViewSet(viewsets.ViewSet):
    authentication_classes = [ParticipantTokenAuthentication]

    def get_permissions(self):
        return [AllowAny()]

    @extend_schema(responses={200: LeaderboardResponseSerializer})
    def list(self, request):
        event_id = request.query_params.get("event_id")
        event_code = request.query_params.get("event_code")
        search_query = request.query_params.get("search")

        student_participant = getattr(request, "participant", None)
        if not student_participant and request.user:
            student_participant = getattr(request.user, "participant", None)

        data = LeaderboardService.get_event_leaderboard(
            event_id=event_id,
            event_code=event_code,
            search_query=search_query,
            student_participant=student_participant,
        )
        return success_response(data=data, message="Leaderboard retrieved successfully.")

    @extend_schema(responses={200: LeaderboardResponseSerializer})
    @action(detail=False, methods=["get"], url_path="current")
    def current(self, request):
        student_participant = getattr(request, "participant", None)
        if not student_participant and request.user:
            student_participant = getattr(request.user, "participant", None)

        if not student_participant:
            return success_response(message="Participant token required for current event leaderboard.", status_code=status.HTTP_401_UNAUTHORIZED)

        data = LeaderboardService.get_event_leaderboard(
            event=student_participant.event,
            student_participant=student_participant,
        )
        return success_response(data=data, message="Current event leaderboard retrieved successfully.")
