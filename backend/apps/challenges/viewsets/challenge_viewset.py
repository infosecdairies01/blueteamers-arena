from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apps.accounts.permissions.is_admin import IsAdmin
from apps.challenges.models.challenge import Challenge
from apps.challenges.selectors.challenge_selector import ChallengeSelector
from apps.challenges.services.challenge_service import ChallengeService
from apps.challenges.serializers.challenge_serializer import ChallengeSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdmin()]

    def get_queryset(self):
        difficulty = self.request.query_params.get("difficulty")
        search_query = self.request.query_params.get("search")
        return ChallengeSelector.filter_challenges(difficulty=difficulty, query=search_query)

    def perform_create(self, serializer):
        challenge = ChallengeService.create_challenge(serializer.validated_data)
        serializer.instance = challenge
