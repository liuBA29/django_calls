#routing.py

from django.urls import path, re_path
from .consumer import WSConsumer, ActiveCallsConsumer, SimpleWebSocketConsumer, CallStatusConsumer

ws_urlpatterns = [
    path('ws/random-number/', WSConsumer.as_asgi()),
    path('ws/active-calls/', ActiveCallsConsumer.as_asgi()),
    path(r'ws/test-socket/', SimpleWebSocketConsumer.as_asgi()),
    path(r'ws/call-status/', CallStatusConsumer.as_asgi()),  # Обработчик WebSocket по адресу /ws/call-status/
]
