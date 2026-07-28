from rest_framework.routers import DefaultRouter
from apps.events.viewsets.event_viewset import EventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")

urlpatterns = router.urls
