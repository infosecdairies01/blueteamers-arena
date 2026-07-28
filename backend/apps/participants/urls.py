from rest_framework.routers import DefaultRouter
from apps.participants.viewsets.participant_viewset import ParticipantViewSet

router = DefaultRouter()
router.register(r"participants", ParticipantViewSet, basename="participant")

urlpatterns = router.urls
