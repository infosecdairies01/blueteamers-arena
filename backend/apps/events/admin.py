from django.contrib import admin
from apps.events.models.event import Event
from apps.events.models.event_question import EventQuestion


class EventQuestionInline(admin.TabularInline):
    model = EventQuestion
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("college_name", "workshop_name", "event_code", "event_date", "status", "created_at")
    list_filter = ("status", "accent_color", "event_date")
    search_fields = ("college_name", "workshop_name", "event_code")
    inlines = [EventQuestionInline]
    ordering = ("-event_date", "-created_at")


@admin.register(EventQuestion)
class EventQuestionAdmin(admin.ModelAdmin):
    list_display = ("event", "question_id", "position", "created_at")
    list_filter = ("event",)
    ordering = ("event", "position")
