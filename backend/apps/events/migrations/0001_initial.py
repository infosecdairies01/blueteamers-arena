import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("college_name", models.CharField(db_index=True, max_length=150)),
                ("workshop_name", models.CharField(max_length=200)),
                ("event_code", models.CharField(db_index=True, max_length=50, unique=True)),
                ("event_date", models.DateField()),
                ("duration_minutes", models.PositiveIntegerField(default=60)),
                ("passing_score", models.PositiveIntegerField(default=600)),
                ("total_challenges", models.PositiveIntegerField(default=5)),
                ("accent_color", models.CharField(default="blue", max_length=20)),
                (
                    "status",
                    models.CharField(
                        choices=[("Upcoming", "Upcoming"), ("Live", "Live"), ("Completed", "Completed")],
                        db_index=True,
                        default="Upcoming",
                        max_length=20,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ["-event_date", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="EventQuestion",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("question_id", models.UUIDField(db_index=True)),
                ("position", models.PositiveIntegerField(default=1)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_questions",
                        to="events.event",
                    ),
                ),
            ],
            options={
                "verbose_name": "Event Question",
                "verbose_name_plural": "Event Questions",
                "ordering": ["position", "created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="event",
            index=models.Index(fields=["event_code"], name="events_even_event_c_123456_idx"),
        ),
        migrations.AddIndex(
            model_name="event",
            index=models.Index(fields=["status"], name="events_even_status_654321_idx"),
        ),
        migrations.AddIndex(
            model_name="event",
            index=models.Index(fields=["college_name"], name="events_even_college_789012_idx"),
        ),
        migrations.AddIndex(
            model_name="eventquestion",
            index=models.Index(fields=["event", "position"], name="events_even_event_i_345678_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="eventquestion",
            unique_together={("event", "question_id")},
        ),
    ]
