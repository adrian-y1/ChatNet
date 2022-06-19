import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoomMessage, User, PublicChatRoomMessage
from channels.db import database_sync_to_async
from django.utils import timezone
import datetime
import markdown2
from markdown2 import Markdown
markdowner = Markdown()

class ChatConsumer(AsyncWebsocketConsumer):

    # Obtain the 'room_name' paramater form the URL route in routing.py that opened the WebSocket connection to the consumer
    # Every consumer has a scope that containers information about its connection, including any positional or kwargs from the URL route and currently authenticated user.
    async def connect(self):
        self.other_user = self.scope['url_route']["kwargs"]["id"]
        self.current_user = self.scope["user"].id

        if int(self.current_user) > int(self.other_user):
            self.room_name = f"{self.current_user}-{self.other_user}"
        else:
            self.room_name = f"{self.other_user}-{self.current_user}"

        # This line constructs a Channels group name directly from the user-specified room name, without any quoting or escaping. 
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        # async_to_sync is a wrapper that is calling an asynchronous channel lyaer method because ChatConsumer is a synchronous WebSocketConsumer
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # This accepts the WebSocket connection. If you dont call .accept() within connect() method then the connection will be closed and rejected.
        # You can use this to an advantage of whereby if the requested user is not authorised to perform the requested action
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        if message != '' and message != ' ' and message != '# ' and message != '## ' and message != '### ':
            get_user_instance = await self.message_sender(username)
            chat_messages = await self.save_messages(self.room_name, markdowner.convert(message), get_user_instance)

        # Send message/event to room group
        # An event has a special 'type' key corresponding to the name of the method that should be invoked on consumers that recieve the event.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                "username": username,
            }
        )

    # Query for the user instance
    @database_sync_to_async
    def message_sender(request, username):
        return User.objects.get(username=username)

    # save the messages that are received through the Websocket in regards to the kwargs given
    @database_sync_to_async
    def save_messages(request, room_name, content, user_name):
        messages = ChatRoomMessage(room_name=room_name, content=content, user=user_name, date_sent=datetime.datetime.utcnow())
        messages.save()
        return messages
   
    def serialise(self):
        return {
            'serialised_time': datetime.datetime.now().strftime("%I:%M %p")
        }

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event["username"]
        
        # Send message to WebSocket
        if message != '' and message != ' ' and message != '# ' and message != '## ' and message != '### ':
            await self.send(text_data=json.dumps({
            'message': markdowner.convert(message),
            "username": username,
            "current_time": self.serialise()["serialised_time"]
        }))


class PublicChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_%s' % ''

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # This accepts the WebSocket connection. If you dont call .accept() within connect() method then the connection will be closed and rejected.
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        current_user_img = await self.user_img(username)

        if message != "" and message != ' ' and message != '# ' and message != '## ' and message != '### ':
            user_instance = await self.global_message_sender(username)
            chat_messages = await self.save_global_messages(markdowner.convert(message), user_instance)

        # Send message/event to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                "username": username,
                "img": current_user_img,
            }
        )

    @database_sync_to_async
    def global_message_sender(request, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def save_global_messages(request, content, user_name):
        messages = PublicChatRoomMessage(content=content, user=user_name, date_sent=datetime.datetime.utcnow())
        messages.save()
        return messages

    def serialise(self):
        return {
            'serialised_time_g': datetime.datetime.now().strftime("%I:%M %p")
        }

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event["username"]
        current_user_img = await self.user_img(username)

        # Send message to WebSocket
        if message != '' and message != ' ' and message != '# ' and message != '## ' and message != '### ':
            await self.send(text_data=json.dumps({
            'message': markdowner.convert(message),
            "username": username,
            "img": current_user_img,
            "current_time": self.serialise()["serialised_time_g"]
        }))

    @database_sync_to_async
    def user_img(request, username):
        user_obj = User.objects.get(username=username)
        return user_obj.profile.picture.url