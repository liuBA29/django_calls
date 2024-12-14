"""
ASGI config for panch_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.urls import path
from configurations.consumer import *
from configurations.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panch_project.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': SessionMiddlewareStack(
        URLRouter(ws_urlpatterns)
    )
})