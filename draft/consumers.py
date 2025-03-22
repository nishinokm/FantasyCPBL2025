import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class DraftConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.draft_id = self.scope['url_route']['kwargs']['draft_id']
        self.group_name = f'draft_{self.draft_id}'
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'chat':
            await self.handle_chat(data)

    async def handle_chat(self, data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': data.get('message'),
                'user': self.user.username if self.user and self.user != AnonymousUser else '匿名',
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'user': event['user']
        }))