import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ArenaConsumer(AsyncWebsocketConsumer):
    """
    WebSocket Consumer for real-time live competition events (Leaderboard updates, Submissions, Top 3 changes).
    URL: /ws/arena/<event_code>/
    """
    async def connect(self):
        self.event_code = self.scope["url_route"]["kwargs"].get("event_code", "global").lower()
        self.group_name = f"event_{self.event_code}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "event": "connected",
            "message": f"Connected to live arena stream for event '{self.event_code}'.",
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Echo back client messages if needed
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            "event": "ack",
            "payload": data,
        }))

    async def broadcast_event(self, event):
        await self.send(text_data=json.dumps({
            "event": event["event"],
            "data": event["data"],
        }))
