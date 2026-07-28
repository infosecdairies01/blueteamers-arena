import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0001_initial"),
        ("challenges", "0001_initial"),
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ParticipantProgress",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("not_started", "Not Started"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                        ],
                        db_index=True,
                        default="not_started",
                        max_length=20,
                    ),
                ),
                ("current_question_index", models.PositiveIntegerField(default=0)),
                ("visited_questions", models.JSONField(blank=True, default=list)),
                ("score_earned", models.PositiveIntegerField(default=0)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, db_index=True, null=True)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participant_progresses",
                        to="challenges.challenge",
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="challenge_progresses",
                        to="participants.participant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Participant Progress",
                "verbose_name_plural": "Participant Progresses",
                "ordering": ["challenge__challenge_number"],
            },
        ),
        migrations.CreateModel(
            name="ParticipantDraftAnswer",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("answer_text", models.TextField(blank=True, default="")),
                ("selected_options", models.JSONField(blank=True, default=list)),
                ("selected_option_index", models.IntegerField(blank=True, null=True)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participant_drafts",
                        to="challenges.challenge",
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="draft_answers",
                        to="participants.participant",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participant_drafts",
                        to="questions.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Participant Draft Answer",
                "verbose_name_plural": "Participant Draft Answers",
            },
        ),
        migrations.AddIndex(
            model_name="participantprogress",
            index=models.Index(fields=["participant", "challenge"], name="partic_prog_p_c_idx"),
        ),
        migrations.AddIndex(
            model_name="participantprogress",
            index=models.Index(fields=["participant", "status"], name="partic_prog_p_s_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="participantprogress",
            unique_together={("participant", "challenge")},
        ),
        migrations.AddIndex(
            model_name="participantdraftanswer",
            index=models.Index(fields=["participant", "challenge"], name="partic_draft_p_c_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="participantdraftanswer",
            unique_together={("participant", "challenge", "question")},
        ),
    ]
