import os
import logging
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from CryptomusWebApp.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CryptomusWebApp.settings')

logger = logging.getLogger('django')

try:
    application = ProtocolTypeRouter({
        "http": get_asgi_application(),  # Для HTTP-запросов
        "websocket": AuthMiddlewareStack(  # Для WebSocket-запросов
            URLRouter(websocket_urlpatterns)
        ),
    })
except Exception as e:
    logger.error(f"Ошибка в ASGI приложении: {e}")
