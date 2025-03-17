from django.urls import re_path
from .consumers import QuizConsumer

websocket_urlpatterns = [
    re_path('ws/quiz/', QuizConsumer.as_asgi()),
]
