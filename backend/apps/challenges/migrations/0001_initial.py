import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Challenge",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("challenge_number", models.PositiveIntegerField(db_index=True, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("brief", models.TextField()),
                (
                    "difficulty",
                    models.CharField(
                        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
                        default="Easy",
                        max_length=20,
                    ),
                ),
                ("duration_minutes", models.PositiveIntegerField(default=20)),
                ("points", models.PositiveIntegerField(default=100)),
                ("skills", models.JSONField(blank=True, default=list)),
                ("objectives", models.JSONField(blank=True, default=list)),
            ],
            options={
                "verbose_name": "Challenge",
                "verbose_name_plural": "Challenges",
                "ordering": ["challenge_number"],
            },
        ),
        migrations.CreateModel(
            name="Evidence",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("artifact_key", models.CharField(db_index=True, max_length=100)),
                ("label", models.CharField(max_length=150)),
                ("filename", models.CharField(max_length=150)),
                (
                    "file_format",
                    models.CharField(
                        choices=[
                            ("TXT", "Text File"),
                            ("LOG", "Log File"),
                            ("JSON", "JSON Data"),
                            ("CSV", "CSV Table"),
                            ("PNG", "PNG Image"),
                        ],
                        default="TXT",
                        max_length=10,
                    ),
                ),
                ("content_text", models.TextField(blank=True, null=True)),
                ("image_url", models.CharField(blank=True, max_length=500, null=True)),
                ("file_size_display", models.CharField(default="4 KB", max_length=50)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evidence_files",
                        to="challenges.challenge",
                    ),
                ),
            ],
            options={
                "verbose_name": "Evidence File",
                "verbose_name_plural": "Evidence Files",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="ChallengeQuestion",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("position", models.PositiveIntegerField(default=1)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="challenge_questions",
                        to="challenges.challenge",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_challenges",
                        to="questions.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Challenge Question",
                "verbose_name_plural": "Challenge Questions",
                "ordering": ["position", "created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="challenge",
            index=models.Index(fields=["slug"], name="challenges__slug_123456_idx"),
        ),
        migrations.AddIndex(
            model_name="challenge",
            index=models.Index(fields=["challenge_number"], name="challenges__challen_654321_idx"),
        ),
        migrations.AddIndex(
            model_name="challenge",
            index=models.Index(fields=["difficulty"], name="challenges__difficu_789012_idx"),
        ),
        migrations.AddIndex(
            model_name="evidence",
            index=models.Index(fields=["challenge", "artifact_key"], name="challenges__challen_345678_idx"),
        ),
        migrations.AddIndex(
            model_name="evidence",
            index=models.Index(fields=["file_format"], name="challenges__file_fo_901234_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="evidence",
            unique_together={("challenge", "artifact_key")},
        ),
        migrations.AddIndex(
            model_name="challengequestion",
            index=models.Index(fields=["challenge", "position"], name="challenges__challen_567890_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="challengequestion",
            unique_together={("challenge", "question")},
        ),
    ]
