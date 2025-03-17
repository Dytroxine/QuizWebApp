from django.shortcuts import render
from quiz.models import Quiz, User
from math import ceil
from django.db import models
from django.http import HttpResponse
from django.contrib.auth import login


def home(request):
    quiz = Quiz.objects.filter(is_displayed=True).first()
    if quiz:
        total_time_in_seconds = quiz.questions.aggregate(
            total_time=models.Sum('time_limit')
        )['total_time'] or 0
        duration_in_minutes = ceil(total_time_in_seconds / 60)
        quiz.duration_in_minutes = duration_in_minutes

    response = render(request, 'main_page/home.html', {'quiz': quiz})
    response['ngrok-skip-browser-warning'] = 'true'  # Добавляем заголовок для обхода предупреждения
    return response


def authenticate_user(request):
    quiz = Quiz.objects.filter(is_displayed=True).first()

    if quiz:
        total_time_in_seconds = quiz.questions.aggregate(
            total_time=models.Sum('time_limit')
        )['total_time'] or 0
        duration_in_minutes = ceil(total_time_in_seconds / 60)
        quiz.duration_in_minutes = duration_in_minutes

    telegram_id = request.GET.get('user_id')

    # Инициализация переменной user
    user = None

    if telegram_id:
        user, created = User.objects.get_or_create(telegram_id=telegram_id)

    response = render(request, 'main_page/home.html', {'quiz': quiz, 'user': user})
    response['ngrok-skip-browser-warning'] = 'true'  # Добавляем заголовок для обхода предупреждения
    return response


