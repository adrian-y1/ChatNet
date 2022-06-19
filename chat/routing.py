from django.urls import re_path

from . import consumers

# as_agi() function returns an ASGI wrapper application that will instantiate a new consumer instance for each connection or scope
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/', consumers.PublicChatConsumer.as_asgi()),
]