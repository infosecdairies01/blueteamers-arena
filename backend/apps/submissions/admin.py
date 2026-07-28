from django.contrib import admin
from apps.submissions.models.submission import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("participant", "challenge", "score_earned", "max_possible_score", "is_passing", "submitted_at")
    list_filter = ("is_passing", "challenge")
    search_fields = ("participant__name", "participant__email", "challenge__name")
    ordering = ("-submitted_at",)
