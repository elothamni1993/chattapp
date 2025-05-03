import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]
        message = data['message']

        await self.save_message(user, message)

        await self.channel_layer.group_send("chat", {
            'type': 'chat_message',
            'message': message,
            'user': user.username,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
        }))

    @sync_to_async
    def save_message(self, user, message):
        Message.objects.create(user=user, content=message)
