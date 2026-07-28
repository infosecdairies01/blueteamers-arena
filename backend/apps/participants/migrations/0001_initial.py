import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Participant",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(db_index=True, max_length=254)),
                ("score", models.PositiveIntegerField(db_index=True, default=0)),
                ("completed", models.PositiveIntegerField(default=0)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, db_index=True, null=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participants",
                        to="events.event",
                    ),
                ),
            ],
            options={
                "verbose_name": "Participant",
                "verbose_name_plural": "Participants",
                "ordering": ["-score", "finished_at", "-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="participant",
            index=models.Index(fields=["event", "email"], name="participant_event_i_123456_idx"),
        ),
        migrations.AddIndex(
            model_name="participant",
            index=models.Index(fields=["event", "score"], name="participant_event_i_654321_idx"),
        ),
        migrations.AddIndex(
            model_name="participant",
            index=models.Index(fields=["score", "finished_at"], name="participant_score_789012_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="participant",
            unique_together={("event", "email")},
        ),
    ]
