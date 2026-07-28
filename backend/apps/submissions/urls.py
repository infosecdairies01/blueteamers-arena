from rest_framework.routers import DefaultRouter
from apps.submissions.viewsets.submission_viewset import SubmissionViewSet

router = DefaultRouter()
router.register(r"submissions", SubmissionViewSet, basename="submission")

urlpatterns = router.urls
