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
            name="AuditLog",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "action_type",
                    models.CharField(
                        choices=[
                            ("LOGIN", "Login"),
                            ("LOGOUT", "Logout"),
                            ("QUESTION_CREATE", "Question Create"),
                            ("QUESTION_UPDATE", "Question Update"),
                            ("EVENT_UPDATE", "Event Update"),
                            ("PARTICIPANT_ACTION", "Participant Action"),
                            ("ADMIN_ACTION", "Admin Action"),
                        ],
                        db_index=True,
                        max_length=50,
                    ),
                ),
                ("description", models.TextField()),
                ("ip_address", models.CharField(blank=True, max_length=45, null=True)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("timestamp", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="audit_logs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Audit Log",
                "verbose_name_plural": "Audit Logs",
                "ordering": ["-timestamp"],
            },
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["action_type"], name="audit_log_action__idx"),
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["timestamp"], name="audit_log_timesta_idx"),
        ),
    ]
