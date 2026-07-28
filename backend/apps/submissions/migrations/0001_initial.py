import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("participants", "0002_participant_progress_and_draft"),
        ("challenges", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("answers_json", models.JSONField(default=dict)),
                ("score_earned", models.PositiveIntegerField(default=0)),
                ("max_possible_score", models.PositiveIntegerField(default=100)),
                ("is_passing", models.BooleanField(default=False)),
                ("evaluation_results", models.JSONField(blank=True, default=list)),
                ("submitted_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="challenges.challenge",
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="participants.participant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Submission",
                "verbose_name_plural": "Submissions",
                "ordering": ["-submitted_at"],
            },
        ),
        migrations.AddIndex(
            model_name="submission",
            index=models.Index(fields=["participant", "challenge"], name="submissions_part_chal_idx"),
        ),
        migrations.AddIndex(
            model_name="submission",
            index=models.Index(fields=["submitted_at"], name="submissions_sub_at_idx"),
        ),
    ]
