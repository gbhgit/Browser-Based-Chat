import json
from datetime import datetime
from django.test import TestCase

import pytest
from channels.testing import WebsocketCommunicator
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatRoom, User

class ProjectTestCase(TestCase):
    def setUp(self):
        self.rooms = []
        User.objects.create_user('testUser', password='12345')
        self.rooms.append( ChatRoom.objects.create(room_name="Work").id )
        self.rooms.append( ChatRoom.objects.create(room_name="Stock").id )
        self.client.login(username='testUser', password='12345')

    def test_chat_get_all_room_posts(self):
        for room in self.rooms:
            response = self.client.post('/get_all_room_posts', {'room_id': room}, follow=True)
            self.assertEqual(200, response.status_code)
    
    def test_chat_redirect_to_room(self):
        for room in self.rooms:
            response = self.client.get('/'+str(room), follow=True)
            self.assertEqual(200, response.status_code)

    @pytest.mark.django_db
    @pytest.mark.asyncio
    async def test_websocket_consumer(self):
        
        results = {}

        class ServerTest(AsyncWebsocketConsumer):
            async def connect(self):
                self.room_id = 1
                self.room_group = 'chat_%s' % self.room_id
                await self.channel_layer.group_add(self.room_group, self.channel_name)
                await self.accept()
            
            async def disconnect(self, close_code):
                await self.channel_layer.group_discard(self.room_group, self.channel_name)
                results["disconnected"] = self.room_group
            
            async def receive(self, text_data):
                data = json.loads(text_data)
                await self.channel_layer.group_send( self.room_group,
                    {
                        'type': 'send_message',
                        'message': data['message'],
                        'user_name': data['user_name'],
                        'created_date': datetime.now().strftime('%Y-%m-%d'), 
                        'created_time': datetime.now().strftime('%H:%M')
                    }
                )
    
            async def send_message(self, event):
                await self.send(text_data=json.dumps({
                    'message': event['message'],
                    'user_name': event['user_name'],
                    'created_date': event['created_date'],
                    'created_time': event['created_time']
                }))
        
        app = ServerTest()
        # Test a normal connection
        communicator = WebsocketCommunicator(app, "/1/")
        connected, _ = await communicator.connect()
        # Test sending text
        await communicator.send_to(text_data=json.dumps(
        {   'message': 'Hello',
            'user_id': 1,
            'room_id': 1,
            'user_name': 'testUser'
        }))
        # Test recive out message
        response = await communicator.receive_from()
        assert 'message' in response 
        assert 'user_name' in response 
        assert 'created_date' in response 
        assert 'created_time' in response 
        # Close out
        await communicator.disconnect()
        assert "disconnected" in results