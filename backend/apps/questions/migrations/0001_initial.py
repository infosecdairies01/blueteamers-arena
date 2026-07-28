import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Phishing", "Phishing"),
                            ("SIEM", "SIEM"),
                            ("AI", "AI"),
                            ("Incident Response", "Incident Response"),
                            ("Digital Forensics", "Digital Forensics"),
                        ],
                        db_index=True,
                        max_length=50,
                    ),
                ),
                (
                    "difficulty",
                    models.CharField(
                        choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[("text", "Text Input"), ("mcq", "Multiple Choice")],
                        default="text",
                        max_length=10,
                    ),
                ),
                ("question_text", models.TextField()),
                ("evidence_text", models.TextField(blank=True, null=True)),
                ("options_json", models.JSONField(blank=True, default=list)),
                ("correct_answer", models.TextField(blank=True, default="")),
                ("correct_option_index", models.IntegerField(blank=True, default=0, null=True)),
                ("explanation", models.TextField(blank=True, null=True)),
                ("default_points", models.PositiveIntegerField(default=10)),
                (
                    "status",
                    models.CharField(
                        choices=[("Draft", "Draft"), ("Published", "Published")],
                        db_index=True,
                        default="Published",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(fields=["category"], name="questions_q_categor_123456_idx"),
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(fields=["difficulty"], name="questions_q_difficu_654321_idx"),
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(fields=["status"], name="questions_q_status_789012_idx"),
        ),
    ]
