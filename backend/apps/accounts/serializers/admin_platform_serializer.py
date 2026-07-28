from rest_framework import serializers


class BulkImportQuestionsSerializer(serializers.Serializer):
    questions = serializers.ListField(child=serializers.DictField(), required=True)


class ExportReportRequestSerializer(serializers.Serializer):
    event_id = serializers.UUIDField(required=False, allow_null=True)
    format = serializers.ChoiceField(choices=["csv", "json"], default="csv")
