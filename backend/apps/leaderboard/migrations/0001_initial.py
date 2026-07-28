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
            name="LeaderboardSnapshot",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("rank_data", models.JSONField(default=list)),
                ("snapshot_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leaderboard_snapshots",
                        to="events.event",
                    ),
                ),
            ],
            options={
                "verbose_name": "Leaderboard Snapshot",
                "verbose_name_plural": "Leaderboard Snapshots",
                "ordering": ["-snapshot_at"],
            },
        ),
    ]
