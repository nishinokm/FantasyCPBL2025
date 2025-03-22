# draft/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DraftConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.draft_id = self.scope['url_route']['kwargs']['draft_id']
        self.group_name = f'draft_{self.draft_id}'

        # 加入群組
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        user = self.scope["user"].username

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': user,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))
