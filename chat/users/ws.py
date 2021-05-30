import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Post, ChatRoom, User

class Server(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group = 'chat_%s' % self.room_id
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.save_post(data['user_id'], data['room_id'], data['message'])
        await self.channel_layer.group_send( self.room_group,
            {
                'type': 'send_message',
                'message': data['message'],
                'user_id': data['user_id']
            }
        )
    
    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id']
        }))

    @sync_to_async
    def save_post(self, user_id, room_id, message):
        # check if has command in message to create bot
        room = ChatRoom.objects.get(pk=room_id)
        user = User.objects.get(pk=user_id)
        post = Post.objects.create(room=room, msn=message, created_by=user)
        post.save()