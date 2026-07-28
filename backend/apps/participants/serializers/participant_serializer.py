from rest_framework import serializers
from apps.participants.models.participant import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source="event.college_name", read_only=True)
    event_code = serializers.CharField(source="event.event_code", read_only=True)

    class Meta:
        model = Participant
        fields = [
            "id",
            "event",
            "college_name",
            "event_code",
            "name",
            "email",
            "score",
            "completed",
            "started_at",
            "finished_at",
            "created_at",
        ]
        read_only_fields = ["id", "score", "completed", "started_at", "finished_at", "created_at"]


class RegisterStudentSerializer(serializers.Serializer):
    event_id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
