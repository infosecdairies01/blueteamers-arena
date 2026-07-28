from django.db import models
from apps.common.models.base import BaseModel
from apps.events.models.event import Event


class LeaderboardSnapshot(BaseModel):
    """
    Stores historical ranking snapshots for live events.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="leaderboard_snapshots")
    rank_data = models.JSONField(default=list)
    snapshot_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Leaderboard Snapshot"
        verbose_name_plural = "Leaderboard Snapshots"
        ordering = ["-snapshot_at"]

    def __str__(self):
        return f"{self.event.event_code} Leaderboard Snapshot at {self.snapshot_at}"
