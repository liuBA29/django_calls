#routing.py

from django.urls import path
from .consumer import WSConsumer, ActiveCallsConsumer, SimpleWebSocketConsumer

ws_urlpatterns = [
    path('ws/random-number/', WSConsumer.as_asgi()),
    path('ws/active-calls/', ActiveCallsConsumer.as_asgi()),
    path(r'ws/test-socket/', SimpleWebSocketConsumer.as_asgi()),
]