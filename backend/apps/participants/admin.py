from django.contrib import admin
from apps.participants.models.participant import Participant
from apps.participants.models.participant_progress import ParticipantProgress
from apps.participants.models.participant_draft import ParticipantDraftAnswer


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "event", "score", "completed", "started_at", "finished_at", "created_at")
    list_filter = ("event", "completed")
    search_fields = ("name", "email", "event__event_code", "event__college_name")
    ordering = ("-score", "finished_at", "-created_at")


@admin.register(ParticipantProgress)
class ParticipantProgressAdmin(admin.ModelAdmin):
    list_display = ("participant", "challenge", "status", "current_question_index", "score_earned", "started_at", "completed_at")
    list_filter = ("status", "challenge")
    search_fields = ("participant__name", "participant__email", "challenge__slug")


@admin.register(ParticipantDraftAnswer)
class ParticipantDraftAnswerAdmin(admin.ModelAdmin):
    list_display = ("participant", "challenge", "question", "updated_at")
    list_filter = ("challenge",)
    search_fields = ("participant__name", "participant__email", "answer_text")
