from django.urls import path, include

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("", include("apps.events.urls")),
    path("", include("apps.participants.urls")),
    path("", include("apps.questions.urls")),
    path("", include("apps.challenges.urls")),
]
