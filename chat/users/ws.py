import json
import csv
import time
import requests
from io import StringIO
from datetime import datetime
from .models import Post, ChatRoom, User

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class BOT:
    def __init__(self):
        self.name = 'bot'
        self.queue = []
    def stock(self, param):
        r = requests.get('https://stooq.com/q/l/?s={}&f=sd2t2ohlcv&h&e=csv%E2%80%8B'.format(param))
        row = next( csv.DictReader( StringIO(r.text) ) )
        if row['Close'] == 'N/D':
            return 'Error: Command not have quote'
        else:   
            return '{} quote is ${} per share'.format(row['Symbol'], row['Close'])
    def deploy(self, command):
        stock_cmd = command.split("=")
        current_time = datetime.now()
        response = {
            'user_name': self.name, 
            'created_date': current_time.strftime('%Y-%m-%d'), 
            'created_time': current_time.strftime('%H:%M')
        }
        
        if len(stock_cmd) != 2:
            response['message'] = 'Error: Wrong command'
        else:
            if stock_cmd[0] == 'stock' and len(stock_cmd[1]) > 1:
                job_id = len(self.queue) - 1
                self.queue.append( [job_id, stock_cmd[1], 'created'] )
                if len(self.queue) >= 2:
                    while self.queue[job_id - 1][0] == 'created':
                        time.sleep(0.5)
                    self.queue[job_id][2] = 'finished'
                    response['message'] = self.stock(stock_cmd[1])
                elif len(self.queue) == 1:
                    self.queue[0][2] = 'finished'
                    response['message'] = self.stock(stock_cmd[1])
            else:
                response['message'] = 'Error: Wrong command {}'.format(stock_cmd[0])
        return response

bot = BOT()

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
        out = await self.save_post(data['user_name'], data['user_id'], data['room_id'], data['message'])
        await self.channel_layer.group_send( self.room_group,
            {
                'type': 'send_message',
                'message': out['message'],
                'user_name': out['user_name'],
                'created_date': out['created_date'],
                'created_time': out['created_time']
            }
        )
    
    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_name': event['user_name'],
            'created_date': event['created_date'],
            'created_time': event['created_time']
        }))

    @sync_to_async
    def save_post(self, user_name, user_id, room_id, message):
        if message[:1] == '/': # maybe bot
            return bot.deploy(message[1:])
        else:
            room = ChatRoom.objects.get(pk=room_id)
            user = User.objects.get(pk=user_id)
            post = Post.objects.create(room=room, msn=message, created_by=user)
            post.save()
            return {
                'message': message,
                'user_name': user_name, 
                'created_date': post.created.strftime('%Y-%m-%d'), 
                'created_time': post.created.strftime('%H:%M')
            }