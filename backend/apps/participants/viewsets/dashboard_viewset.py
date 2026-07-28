from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema
from apps.common.utils.response import success_response
from apps.participants.auth.participant_auth import ParticipantTokenAuthentication
from apps.participants.permissions.is_participant import IsParticipant
from apps.participants.services.dashboard_service import DashboardService
from apps.participants.serializers.dashboard_serializer import DashboardSerializer


class DashboardViewSet(viewsets.ViewSet):
    authentication_classes = [ParticipantTokenAuthentication]
    permission_classes = [IsParticipant]

    @extend_schema(responses={200: DashboardSerializer})
    def list(self, request):
        participant = getattr(request, "participant", None)
        if not participant and request.user:
            participant = getattr(request.user, "participant", None)

        if not participant:
            return success_response(message="Participant authentication required.", status_code=status.HTTP_401_UNAUTHORIZED)

        dashboard_data = DashboardService.get_student_dashboard(participant)
        return success_response(data=dashboard_data, message="Dashboard metrics retrieved successfully.")
