from rest_framework.routers import DefaultRouter
from apps.challenges.viewsets.challenge_viewset import ChallengeViewSet

router = DefaultRouter()
router.register(r"challenges", ChallengeViewSet, basename="challenge")

urlpatterns = router.urls
