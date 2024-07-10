
# from django.urls import path
# # from channels.http import AsgiHandler
# from channels.routing import ProtocolTypeRouter, URLRouter
# from . import consumers

# websocket_urlpatterns = [
#     path('ws/sc/<str:groupkaname>/', consumers.EchoConsumer.as_asgi()),
#     path('ws/sc/', consumers.EchoConsumer.as_asgi()),

#     path('ws/ac/', consumers.asyncEchoConsumer.as_asgi()),
# ]
# myapp/routing.py
from django.urls import path
from . import consumer
websocket_urlpatterns = [
    path('ws/sc/hello/', consumer.asyncEchoConsumer.as_asgi()),
    # path('ws/sc/<str:groupkaname>/', consumer.ChatConsumer.as_asgi()),

    path('ws/sc/<str:groupkaname>/', consumer.EchoConsumer.as_asgi()),

]
