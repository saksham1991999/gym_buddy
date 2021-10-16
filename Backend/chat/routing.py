from django.urls import re_path

from .consumers import room_chat

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', room_chat.ChatConsumer.as_asgi()),
]