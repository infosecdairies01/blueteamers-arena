from django.contrib import admin
from apps.leaderboard.models.leaderboard_snapshot import LeaderboardSnapshot


@admin.register(LeaderboardSnapshot)
class LeaderboardSnapshotAdmin(admin.ModelAdmin):
    list_display = ("event", "snapshot_at")
    list_filter = ("event",)
    ordering = ("-snapshot_at",)
