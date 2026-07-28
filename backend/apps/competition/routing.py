from django.urls import re_path
from apps.competition.consumers.arena_consumer import ArenaConsumer

websocket_urlpatterns = [
    re_path(r"ws/arena/(?P<event_code>\w+)/$", ArenaConsumer.as_asgi()),
]
