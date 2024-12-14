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


class ActiveCallsConsumer(AsyncWebsocketConsumer):

    # Подключение WebSocket
    async def connect(self):
        self.room_name = "active_calls"  # Имя комнаты для всех подключенных клиентов
        self.room_group_name = f"active_calls_{self.room_name}"

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Отправляем начальные данные о звонке
        call_status = await self.get_call_status()
        await self.send(text_data=json.dumps(call_status))

    # Отключение WebSocket
    async def disconnect(self, close_code):
        # Удаляем клиента из группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение состояния звонка
    async def get_call_status(self):
        # Получаем данные о текущем звонке
        call_status = await database_sync_to_async(get_call_status)(None)
        call_data = call_status.content.decode("utf-8")
        return json.loads(call_data)

    # Получение сообщений от WebSocket
    async def receive(self, text_data):
        pass

    # Получение обновлений для всех клиентов в группе
    async def send_update(self, event):
        # Отправляем обновления всем подключенным клиентам
        await self.send(text_data=json.dumps(event["message"]))



class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        for i in range(1000):
            await self.send(json.dumps({'message': randint(1, 100)}))
            await asyncio.sleep(1)  # заменяем sleep на асинхронную паузу