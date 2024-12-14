from django.urls import path
from .consumer import WSConsumer

ws_urlpatterns = [
    path('ws/random-number/', WSConsumer.as_asgi()),
]