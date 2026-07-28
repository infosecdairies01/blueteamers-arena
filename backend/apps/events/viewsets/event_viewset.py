from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from apps.common.utils.response import success_response
from apps.accounts.permissions.is_admin import IsAdmin
from apps.events.models.event import Event
from apps.events.selectors.event_selector import EventSelector
from apps.events.services.event_service import EventService
from apps.events.serializers.event_serializer import EventSerializer, VerifyEventCodeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "verify_code"]:
            return [AllowAny()]
        return [IsAdmin()]

    def get_queryset(self):
        status_filter = self.request.query_params.get("status")
        search_query = self.request.query_params.get("search")
        return EventSelector.filter_events(status=status_filter, query=search_query)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        event = EventService.create_event(serializer.validated_data, user=user)
        serializer.instance = event

    @extend_schema(request=VerifyEventCodeSerializer, responses={200: EventSerializer})
    @action(detail=False, methods=["post"], url_path="verify-code", permission_classes=[AllowAny])
    def verify_code(self, request):
        serializer = VerifyEventCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = EventService.verify_event_code(serializer.validated_data["code"])
        return success_response(
            data=EventSerializer(event).data,
            message="Event code verified successfully.",
        )
