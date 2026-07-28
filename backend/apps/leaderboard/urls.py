from rest_framework.routers import DefaultRouter
from apps.leaderboard.viewsets.leaderboard_viewset import LeaderboardViewSet

router = DefaultRouter()
router.register(r"leaderboard", LeaderboardViewSet, basename="leaderboard")

urlpatterns = router.urls
