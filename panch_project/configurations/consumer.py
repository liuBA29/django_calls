#consumer.py

import asyncio
from channels.generic.websocket import  WebsocketConsumer, AsyncWebsocketConsumer
from random import randint
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from configurations.views import *
import json
from .views import get_call_status
from channels.db import database_sync_to_async
from time import sleep

import json
from channels.generic.websocket import AsyncWebsocketConsumer


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ActiveCallsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Простой вывод в консоль
        print("Попытка подключения WebSocket...")

        # Принять соединение
        await self.accept()

        # Теперь безопасно отправить сообщение
        await self.send(text_data=json.dumps({
            'message': 'Connection successful!'
        }))

    async def disconnect(self, close_code):
        # Логирование отключения
        print("WebSocket disconnected!")

    async def receive(self, text_data):
        # Здесь можно обработать входящие сообщения, но для простоты это пусто
        pass



class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        for i in range(1000):
            await self.send(json.dumps({'message': randint(1, 100)}))
            await asyncio.sleep(1)  # заменяем sleep на асинхронную паузу