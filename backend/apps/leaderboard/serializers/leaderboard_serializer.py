from rest_framework import serializers


class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    participant_id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    college_name = serializers.CharField()
    event_code = serializers.CharField()
    score = serializers.IntegerField()
    completed = serializers.IntegerField()
    time_taken = serializers.CharField()
    is_current_user = serializers.BooleanField()


class LeaderboardResponseSerializer(serializers.Serializer):
    event_code = serializers.CharField()
    college_name = serializers.CharField()
    total_participants = serializers.IntegerField()
    top3_podium = LeaderboardEntrySerializer(many=True)
    rankings = LeaderboardEntrySerializer(many=True)
    student_position = LeaderboardEntrySerializer(allow_null=True)
    nearby_rankings = LeaderboardEntrySerializer(many=True)
