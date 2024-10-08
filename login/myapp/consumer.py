from time import sleep
from channels.consumer import SyncConsumer
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync
from .models import * 
class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("websocket connect.......................................")
        print("in connect")
        print("Channel layer .......................................",self.channel_layer)
        print("Channel name .......................................",self.channel_name)

        print("Group Name...", self.scope ['url_route']['kwargs']['groupkaname'])
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        # add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
        self.group_name, # group name
        self.channel_name
        )
        self.send({'type':'websocket.accept'})




        
    def websocket_receive(self, event):

        print("websocket receive.........................................")
        print("event",event)
        print("event text type",type(event['text']))
        # data=json.loads(event['text'])
        # print("after conversion",data)
        # chat=Message(message_value=event['text'],Channel_Id=self.group_name)
        # chat.save()
        async_to_sync(self.channel_layer.group_send) (
        self.group_name,
        {
        'type': 'chat.message',
        'message': event['text']
        })


    def chat_message(self, event):
        print("in chatmessage")
        print('Event...', event)
        print('Actual Data...', event['message'])
        print('Type of Actual Data...', type(event['message']))
        self.send({
        'type': 'websocket.send',
        'text': event['message']
        })
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.contrib.auth.models import User
from .models import *
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print("71")
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        print(self.group_id)
        self.channel_group_id = f"group_{self.group_id}"
        print(self.channel_group_id)
        token = self.scope['query_string'].decode().split('=')[1]
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        # self.user = await self.get_user(user_id)
        self.user_id=user_id
        print("self.user",self.user_id)
        # print("self.user", self.user.id)
        # print(user_id, "user_id")
        if not self.user_id:
            print("error in 76")
            await self.close(code=4000)
            return "error is occur due to the self.user"
        try:
            channel = await self.get_channel(self.group_id)

            if await self.is_channel_member(self.user_id, self.group_id):
                print("helo i am arqumS",self.is_channel_member(self.user_id, channel))
                await self.channel_layer.group_add(
                    self.channel_group_id,
                    self.channel_name
                )
                await self.accept()
            else:
                print("error in 92")
                await self.close(code=403)
                return "error because the user is not the member of channel"
        except Channel.DoesNotExist:
            print("error in 95")
            await self.close(code=403, reason="Channel is not present")
            return "channel is not preset"

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.channel_group_id,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message'].strip()
            print(message, "message")
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
            return
        except KeyError:
            print("131")
            await self.send(text_data=json.dumps({
                'error': 'Message field is required'
            }))
            return
        print("135")
        print("self.group_name", self.group_id)
        print("message", message)

        await self.channel_layer.group_send(
            self.channel_group_id,  # Use self.channel_group_name
            {
                'type': 'chat_message',  # Correct the message type
                'message': message
            }
        )
        print("147")
        await self.save_message(self.group_id, self.user_id, message)


    async def chat_message(self, event):
        print("151")
        message = event['message']
        print("152")
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id) if user_id else None

    @database_sync_to_async
    def get_user_by_username(self, username):
        return User.objects.get(username=username) if username else None

    @database_sync_to_async
    def get_channel(self, channel_id):
        return Channel.objects.get(id=channel_id)

    @database_sync_to_async
    def is_channel_member(self, user_id, channel_id):
        return ChannelMember.objects.filter(user_id=user_id, channel_id=channel_id).exists()

    @database_sync_to_async
    def save_message(self, channel_id, sender_id, message_value):
        print("167----------------")
        print("channels",channel_id,"sender",sender_id,"message_value",message_value)
        chat = Channel_Message(Channel_Id_id=channel_id, message_sender_id=sender_id, message_value=message_value)
        chat.save()
        return chat

def websocket_disconnect(self, event):
    print("in disconnect")
    print("websocket disconnect........................................")
    print("Channel layer .......................................",self.channel_layer)
    print("Channel name .......................................",self.channel_name)
    async_to_sync(self.channel_layer.group_discard)(
    self.group_name, # group name
    self.channel_name
    )
    raise StopConsumer()



class asyncEchoConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("websocket connect")
        await self.send({'type':'websocket.accept'})



    async def websocket_receive(self, event):
        # await self.send({
        #     "type": "websocket.send",
        #     "text": event["text"],
        # })
        print("websocket receive.........................................",event['text'])
        helo=event['text']
        print(helo)
        for i in range(10):
            await self.send({'type':'websocket.send',
                    'text':f'in async {str(i)} '
                    
                    }
                        )
            # sleep(1)
    async def websocket_disconnect(self, event):
        # self.send({
        #     "type": "websocket.accept",
        # })
        print("websocket disconnect........................................")
        raise StopConsumer()










# import websockets

# import json
# import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from deribit_api import RestClient
# # deribit_project/deribit_app/views.py
# from enum import Enum

# from django.shortcuts import render
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import asyncio
# from asgiref.sync import async_to_sync

# # def index(request):
# #     # Your view logic here
# #     return render(request, 'index.html')

# import requests
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# class WebSocketState(Enum):
#     CONNECTED = "connected"
#     DISCONNECTED = "disconnected"

# class DeribitConsumer(AsyncWebsocketConsumer):
#     websocket_state = WebSocketState.DISCONNECTED
#     async def connect(self):
#         print("Connecting...")
#         await self.accept()
#         self.websocket_state = WebSocketState.CONNECTED
#         # Get instruments and subscribe to their tickers
#         instruments = await self.get_instruments()

#         if instruments is not None:
#             print("sucessfully get the data from website.")
#             await self.subscribe_instruments(instruments)
#         else:
#             print("Failed to get instruments.")
#         await self.websocket_consumer()

#     async def disconnect(self, close_code):
#         print(f"Disconnected with code: {close_code}")
#         self.websocket_state = WebSocketState.DISCONNECTED

#     async def receive(self, text_data=None, bytes_data=None):
#         # Handle received messages if needed
#         if text_data:
#             data = json.loads(text_data)
#             print("Received data:", data)
#             await self.update_table(data)

#     async def get_instruments(self):
#         print("Sending Get Instruments message")
#         message = {
#             "method": "public/get_instruments",
#             "params": {
#                 "currency": "BTC",
#                 "kind": "future"
#             },
#             "jsonrpc": "2.0",
#             "id": 1
#         }

#         async def call_api(msg):
#             async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
#                 await websocket.send(msg)
#                 while websocket.open:
#                     response = await websocket.recv()
#                     # do something with the response...
#                     print("hello", response)
#                     return response  # Assuming the response is a JSON string
#         response = await call_api(json.dumps(message))

#         # Now, parse the response to extract instrument data
#         try:
#             data = json.loads(response)
#             instruments = data.get("result", [])
#             return instruments
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON response: {e}")
#             return None
        
#     async def subscribe_instruments(self, instruments):
#         print("Sending subscribe message")
#         for instrument in instruments:
#             # print("instrument",instrument)
#             message = {
#                 "jsonrpc": "2.0",
#                 "id": 2,
#                 "method": "public/subscribe",
#                 "params": {"channels": [f"ticker.{instrument}.100ms"]},
#             }


            
#             print("subscribe_instruments",message)
#             await self.send(text_data=json.dumps(message))

#     async def websocket_consumer(self):
#         print("websocket_consumer")
#         while self.websocket_state == WebSocketState.CONNECTED:
#             # print("websocket_consumer in")
#             response = await self.receive()
#             print("response",response)
#             # Process the received messages from Deribit (if any)
#             if response is not None:
#                 try:
#                     data = json.loads(response)
#                     await self.update_table(data)
#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON response: {e}")

#             # Add a delay or use other logic as needed
#             await asyncio.sleep(1)
       
#     async def update_table(self, data):
#         # Implement logic to update the HTML table with real-time data
#         # You may use channels to send the data to the connected WebSocket clients
#         print("About to send Data: ", data)

#         # Example of making a private API request to get account summary
#         account_summary = await self.get_account_summary()
#         print("Account Summary:", account_summary)

#         await self.send(text_data=json.dumps(data))

#     async def get_account_summary(self):
#         oauth_url = "https://www.deribit.com/api/v2/public/auth"
#         client_id = "XsKlLLKV"
#         client_secret = "ih4L5FDGJcE4nX4k7Oj52uB5D-6GkYtenwEUzDknPBE"

#         # Get the OAuth token
#         response = requests.post(oauth_url, data={
#             "grant_type": "client_credentials",
#             "client_id": client_id,
#             "client_secret": client_secret,
#         })

#         token = response.json().get("result", {}).get("access_token")

#         if token:
#             private_api_url = "https://www.deribit.com/api/v2/private/get_account_summary"
#             headers = {
#                 "Authorization": f"Bearer {token}",
#             }

#             # Make the API request
#             response = requests.get(private_api_url, headers=headers)

#             # Parse and return the response data
#             return response.json()
#         else:
#             print("Failed to obtain OAuth token")
#             return None



            
    # async def connect(self):
    #     print("connecting...")
    #     await self.accept()

    #     # Get instruments and subscribe to their tickers
    #     instruments = await self.get_instruments()
    #     await self.subscribe_instruments(instruments)

    #     # Start consuming WebSocket messages
    #     await self.websocket_consumer()

    # async def disconnect(self, close_code):
    #     pass  # Handle disconnection if needed

    # async def receive(self, text_data):
    #     pass  # Handle received messages if needed

    # async def get_instruments(self):
    #     print("sending Get Instruments message")
    #     message = {
    #         "jsonrpc": "2.0",
    #         "id": 1,
    #         "method": "public/get_instruments",
    #         "params": {"currency": "BTC", "kind": "future", "expired": False},
    #     }

    #     await self.send(text_data=json.dumps(message))
    #     response = await self.receive()
    #     return json.loads(response)["result"]

    # async def subscribe_instruments(self, instruments):
    #     print("sending subscribe message")
    #     for instrument in instruments:
    #         message = {
    #             "jsonrpc": "2.0",
    #             "id": 2,
    #             "method": "public/subscribe",
    #             "params": {"channels": [f"ticker.{instrument}.100ms"]},
    #         }

    #         await self.send(text_data=json.dumps(message))

    # async def websocket_consumer(self):
    #     while True:
    #         response = await self.receive()
    #         data = json.loads(response)["params"]
    #         await self.update_table(data)

    # async def update_table(self, data):
    #     # Implement logic to update the HTML table with real-time data
    #     # You may use channels to send the data to the connected WebSocket clients
    #     print("About to send Data: ", data)
    #     await self.send(text_data=json.dumps(data))





# class DeribitConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         print("hello")
#         # Connect to Deribit WebSocket
#         self.deribit = RestClient()
#         await self.deribit.ws_connect()
        

#         # Get instruments and subscribe to their updates
#         instruments = await database_sync_to_async(self.deribit.get_instruments)()
#         for instrument in instruments:
#             await self.deribit.subscribe(f"trades.{instrument['instrument_name']}")

#     async def disconnect(self, close_code):
#         await self.deribit.ws_close()
#         print("hello2")

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

#     async def instrument_update(self, event):
#         message = event['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
