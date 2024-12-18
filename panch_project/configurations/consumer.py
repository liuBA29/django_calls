#consumer.py

import asyncio
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .scripts.asterisk_connection import AsteriskConnection
from decouple import config
from random import randint
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from configurations.views import *
from .views import get_call_status
from channels.db import database_sync_to_async
from time import sleep
from channels.layers import get_channel_layer
import json


# Параметры подключения к Asterisk
host = config('ASTERISK_HOST')
port = config('ASTERISK_PORT', cast=int, default=22)
username = config('ASTERISK_USERNAME')
password = config('ASTERISK_PASSWORD')


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'call_status'

        # Проверяем состояние соединения с Asterisk
        self.is_connected = await self.check_asterisk_connection()

        # Принимаем соединение
        await self.accept()

        # Отправляем текущий статус соединения
        await self.send_connection_status()

    async def disconnect(self, close_code):
        # Логика отключения, если потребуется
        pass

    async def receive(self, text_data):
        # Получаем данные от клиента, если нужно
        pass

    async def send_connection_status(self):
        # Отправляем статус соединения в клиент
        await self.send(text_data=json.dumps({
            'is_connected': self.is_connected
        }))

    async def check_asterisk_connection(self):
        # Проверка соединения с Asterisk
        try:
            asterisk_conn = AsteriskConnection(host, port, username, password)
            asterisk_conn.connect()
            if asterisk_conn.check_connection():
                asterisk_conn.close_connection()
                return True
        except Exception as e:
            print(f"Error checking Asterisk connection: {e}")
        return False



class SimpleWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Принимаем WebSocket-соединение
        await self.accept()
        print("WebSocket подключен!")

        # Запускаем периодическую отправку данных
        #self.send_task = asyncio.create_task(self.send_data_periodically())

    async def disconnect(self, close_code):
        # Завершаем задачу при отключении
        if hasattr(self, 'send_task'):
            self.send_task.cancel()
            await asyncio.gather(self.send_task, return_exceptions=True)
        print("WebSocket отключен!")

    async def receive(self, text_data):
        # Получаем сообщение от клиента
        print(f"Сообщение от клиента: {text_data}")
        await self.send(text_data=json.dumps({
            'message': 'Сообщение получено сервером'
        }))

    async def send_data_periodically(self):
        # Периодически отправляем данные клиенту
        while True:
            await self.send(text_data=json.dumps({
                'message': 'Привет! Это сервер :)'
            }))
            await asyncio.sleep(3)  # Каждые 3 секунды отправляем сообщение



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