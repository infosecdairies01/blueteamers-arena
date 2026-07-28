from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    student_profile = serializers.DictField()
    current_event = serializers.DictField()
    current_score = serializers.IntegerField()
    current_rank = serializers.IntegerField()
    completed_challenges = serializers.IntegerField()
    remaining_challenges = serializers.IntegerField()
    leaderboard_position = serializers.IntegerField()
    time_remaining = serializers.DictField()
    recent_activity = serializers.ListField(child=serializers.DictField())
    completion_percentage = serializers.FloatField()
    statistics = serializers.DictField()
