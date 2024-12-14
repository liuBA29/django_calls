#routing.py

from django.urls import path
from .consumer import WSConsumer, ActiveCallsConsumer

ws_urlpatterns = [
    path('ws/random-number/', WSConsumer.as_asgi()),
    path('ws/active-calls/', ActiveCallsConsumer.as_asgi()),
]