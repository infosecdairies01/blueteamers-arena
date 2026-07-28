import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("blueteamers_arena")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Celery Beat Periodic Task Schedules
app.conf.beat_schedule = {
    "cleanup-expired-tokens-every-hour": {
        "task": "apps.common.tasks.cleanup_expired_password_tokens",
        "schedule": crontab(minute=0, hour="*"),
    },
    "auto-start-end-events-every-5-mins": {
        "task": "apps.common.tasks.event_auto_start_end_task",
        "schedule": crontab(minute="*/5"),
    },
    "refresh-live-leaderboards-every-minute": {
        "task": "apps.common.tasks.refresh_live_leaderboards_task",
        "schedule": crontab(minute="*"),
    },
}
