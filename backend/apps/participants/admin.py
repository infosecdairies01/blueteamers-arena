from django.contrib import admin
from apps.participants.models.participant import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "event", "score", "completed", "started_at", "finished_at", "created_at")
    list_filter = ("event", "completed")
    search_fields = ("name", "email", "event__event_code", "event__college_name")
    ordering = ("-score", "finished_at", "-created_at")
