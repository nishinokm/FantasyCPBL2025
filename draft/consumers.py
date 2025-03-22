# draft/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import DraftRoom, DraftUnit
from cpbl_players.models import CPBLPlayer
from fb_leagues.models import FantasyTeam
from django.utils.timezone import now

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
        message_type = data.get('type')

        if message_type == 'chat':
            await self.handle_chat(data)
        elif message_type == 'pick':
            await self.handle_pick(data)

    async def handle_chat(self, data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': data.get('message'),
                'user': self.user.username if self.user and self.user != AnonymousUser else '匿名',
            }
        )

    async def handle_pick(self, data):
        player_id = data.get('player_id')
        player = await database_sync_to_async(self.get_player)(player_id)
        draft = await database_sync_to_async(self.get_draft)()

        # 找到當前要選的人
        current_unit = await database_sync_to_async(self.get_current_unit)(draft)
        if not current_unit or current_unit.player:
            return

        # 驗證是不是這位用戶該選
        if current_unit.new_owner.owner != self.user:
            return

        # 設定選擇內容
        current_unit.player = player
        current_unit.pick_at_time = now()
        await database_sync_to_async(current_unit.save)()

        # 更新輪次與順位
        await database_sync_to_async(self.update_draft_position)(draft)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'draft.pick',
                'round': current_unit.round,
                'pick': current_unit.pick,
                'player_name': player.name,
                'current_round': draft.current_round,
                'current_pick': draft.current_pick,
                'user_id': self.user.id,
            }
        )

    def get_player(self, player_id):
        return CPBLPlayer.objects.filter(id=player_id).first()

    def get_draft(self):
        return DraftRoom.objects.get(id=self.draft_id)

    def get_current_unit(self, draft):
        return DraftUnit.objects.filter(
            draft=draft,
            round=draft.current_round,
            pick=draft.current_pick,
            player__isnull=True
        ).select_related('new_owner__owner').first()

    def update_draft_position(self, draft):
        units = DraftUnit.objects.filter(draft=draft).order_by('round', 'pick')
        for unit in units:
            if unit.player is None:
                draft.current_round = unit.round
                draft.current_pick = unit.pick
                draft.save()
                return
        # 選完了
        draft.is_complete = True
        draft.save()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'user': event['user']
        }))

    async def draft_pick(self, event):
        await self.send(text_data=json.dumps({
            'type': 'pick',
            'round': event['round'],
            'pick': event['pick'],
            'player_name': event['player_name'],
            'current_round': event['current_round'],
            'current_pick': event['current_pick'],
            'user_id': event['user_id']
        }))
