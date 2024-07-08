# backend/routing.py
from django.urls import re_path,path
from . import consumer

websocket_urlpatterns = [
    path('ws/sc/', consumer.ChatConsumer.as_asgi()),

]
