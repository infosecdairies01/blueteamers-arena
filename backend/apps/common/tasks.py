from celery import shared_task
from datetime import date
from django.utils import timezone
from apps.accounts.models.password_reset import PasswordResetToken
from apps.events.models.event import Event
from apps.leaderboard.models.leaderboard_snapshot import LeaderboardSnapshot
from apps.leaderboard.services.leaderboard_service import LeaderboardService
from apps.competition.services.websocket_service import WebSocketService


@shared_task
def cleanup_expired_password_tokens():
    """
    Deletes password reset tokens that have expired.
    """
    deleted_count, _ = PasswordResetToken.objects.filter(expires_at__lt=timezone.now()).delete()
    return f"Cleaned up {deleted_count} expired password reset tokens."


@shared_task
def archive_completed_event_snapshots():
    """
    Takes a final leaderboard snapshot for all completed events.
    """
    completed_events = Event.objects.filter(status=Event.StatusChoices.COMPLETED)
    count = 0
    for ev in completed_events:
        data = LeaderboardService.get_event_leaderboard(event=ev)
        LeaderboardSnapshot.objects.create(event=ev, rank_data=data.get("rankings", []))
        count += 1
    return f"Archived leaderboard snapshots for {count} completed events."


@shared_task
def event_auto_start_end_task():
    """
    Automatically transitions upcoming events to LIVE on their event date,
    and transitions LIVE events to COMPLETED when expired.
    """
    today = date.today()
    started_count = Event.objects.filter(status=Event.StatusChoices.UPCOMING, event_date=today).update(status=Event.StatusChoices.LIVE)

    # Transition completed events
    live_events = Event.objects.filter(status=Event.StatusChoices.LIVE)
    completed_count = 0
    for ev in live_events:
        if ev.event_date < today:
            ev.status = Event.StatusChoices.COMPLETED
            ev.save()
            completed_count += 1

    return f"Auto-started {started_count} events, auto-completed {completed_count} events."


@shared_task
def refresh_live_leaderboards_task():
    """
    Calculates live leaderboard rankings and broadcasts updates via WebSockets for all LIVE events.
    """
    live_events = Event.objects.filter(status=Event.StatusChoices.LIVE)
    refreshed = 0
    for ev in live_events:
        data = LeaderboardService.get_event_leaderboard(event=ev)
        WebSocketService.notify_leaderboard_update(ev.event_code, data)
        refreshed += 1
    return f"Refreshed live leaderboards for {refreshed} live events."
