from rest_framework.routers import DefaultRouter
from apps.questions.viewsets.question_viewset import QuestionViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")

urlpatterns = router.urls
