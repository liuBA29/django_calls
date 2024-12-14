import asyncio
from channels.generic.websocket import  WebsocketConsumer, AsyncWebsocketConsumer
from random import randint
import json
from time import sleep

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(1000):
            self.send(json.dumps({'message': randint(1,100)}))
            sleep(1)
