from datetime import datetime, timedelta
from django.utils import timezone
from typing import Dict, Any


class TimerService:
    """
    Backend-controlled Timer Engine. Computes elapsed time, remaining seconds, and expired status
    strictly from database records to prevent browser refresh resets.
    """
    @staticmethod
    def calculate_time(started_at: datetime, duration_minutes: int) -> Dict[str, Any]:
        if not started_at:
            return {
                "started_at": None,
                "duration_minutes": duration_minutes,
                "remaining_seconds": duration_minutes * 60,
                "is_expired": False,
                "formatted_remaining": f"{duration_minutes}:00",
            }

        now = timezone.now()
        end_time = started_at + timedelta(minutes=duration_minutes)
        remaining_td = end_time - now
        remaining_seconds = max(0, int(remaining_td.total_seconds()))
        is_expired = remaining_seconds == 0

        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        formatted_remaining = f"{minutes:02d}:{seconds:02d}"

        return {
            "started_at": started_at.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_minutes": duration_minutes,
            "remaining_seconds": remaining_seconds,
            "is_expired": is_expired,
            "formatted_remaining": formatted_remaining,
        }
