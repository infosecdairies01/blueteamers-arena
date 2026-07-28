from rest_framework import serializers
from apps.submissions.models.submission import Submission


class SubmitAnswersRequestSerializer(serializers.Serializer):
    answers = serializers.DictField(required=True, help_text="Dictionary mapping question_id or position to answer")


class SubmissionSerializer(serializers.ModelSerializer):
    challenge_name = serializers.CharField(source="challenge.name", read_only=True)
    challenge_slug = serializers.CharField(source="challenge.slug", read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "challenge_name",
            "challenge_slug",
            "score_earned",
            "max_possible_score",
            "is_passing",
            "evaluation_results",
            "submitted_at",
        ]
        read_only_fields = ["id", "score_earned", "max_possible_score", "is_passing", "evaluation_results", "submitted_at"]
