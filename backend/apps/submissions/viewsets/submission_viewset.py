from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema
from apps.common.utils.response import success_response
from apps.participants.auth.participant_auth import ParticipantTokenAuthentication
from apps.participants.permissions.is_participant import IsParticipant
from apps.submissions.selectors.submission_selector import SubmissionSelector
from apps.submissions.serializers.submission_serializer import SubmissionSerializer


class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [ParticipantTokenAuthentication]
    permission_classes = [IsParticipant]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        participant = getattr(self.request, "participant", None)
        if not participant and self.request.user:
            participant = getattr(self.request.user, "participant", None)

        if not participant:
            return Submission.objects.none()

        challenge_id = self.request.query_params.get("challenge_id")
        return SubmissionSelector.get_participant_submissions(participant.id, challenge_id=challenge_id)
