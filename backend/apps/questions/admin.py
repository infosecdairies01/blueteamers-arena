from django.contrib import admin
from apps.questions.models.question import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text_short", "category", "difficulty", "kind", "default_points", "status", "created_at")
    list_filter = ("category", "difficulty", "kind", "status")
    search_fields = ("question_text", "evidence_text", "explanation")
    ordering = ("-created_at",)

    def question_text_short(self, obj):
        return obj.question_text[:60]
    question_text_short.short_description = "Question"
