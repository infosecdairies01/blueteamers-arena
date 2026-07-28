from typing import Dict, Any
from rest_framework.exceptions import NotFound
from apps.challenges.models.evidence import Evidence
from apps.challenges.models.challenge import Challenge


class EvidenceService:
    @staticmethod
    def get_evidence_for_student(challenge: Challenge, artifact_key: str) -> Dict[str, Any]:
        try:
            ev = Evidence.objects.get(challenge=challenge, artifact_key=artifact_key)
        except Evidence.DoesNotExist:
            raise NotFound(f"Evidence artifact '{artifact_key}' not found for challenge '{challenge.slug}'.")

        return {
            "id": str(ev.id),
            "artifact_key": ev.artifact_key,
            "label": ev.label,
            "filename": ev.filename,
            "file_format": ev.file_format,
            "content_text": ev.content_text,
            "image_url": ev.image_url,
            "file_size_display": ev.file_size_display,
            "viewer_type": EvidenceService._determine_viewer_type(ev.file_format),
        }

    @staticmethod
    def _determine_viewer_type(file_format: str) -> str:
        fmt = file_format.upper()
        if fmt == "PNG":
            return "image"
        elif fmt == "JSON":
            return "json"
        elif fmt == "CSV":
            return "csv"
        elif fmt in ["LOG", "TXT"]:
            return "text"
        return "text"
