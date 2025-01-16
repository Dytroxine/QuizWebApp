from django.urls import path
from . import views

urlpatterns = [
    path('bot_register/', views.bot_register, name='bot_register'),
]
