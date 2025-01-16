import hashlib
import hmac
import time
from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth import login
from .models import User

def telegram_login(request):
    # Получение данных из запроса
    telegram_data = request.GET
    hash_value = telegram_data.get('hash')

    # Проверка обязательных параметров
    if not hash_value or 'id' not in telegram_data:
        return HttpResponseBadRequest('Invalid request parameters')

    # Сортировка и преобразование данных в строку
    data_check_string = '\n'.join(
        [f"{k}={v}" for k, v in sorted(telegram_data.items()) if k != 'hash']
    )

    # Проверка подписи, используя секретный ключ бота
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != hash_value:
        return HttpResponseBadRequest('Data integrity check failed')

    # Проверка срока действия данных
    auth_date = int(telegram_data.get('auth_date', 0))
    if time.time() - auth_date > 86400:
        return HttpResponseBadRequest('Data is too old')

    # Создание или обновление пользователя в БД
    telegram_id = telegram_data['id']
    user, created = User.objects.get_or_create(telegram_id=telegram_id)
    user.username = telegram_data.get('username', f'telegram_user_{telegram_id}')
    user.first_name = telegram_data.get('first_name', '')
    user.last_name = telegram_data.get('last_name', '')
    user.save()

    # Авторизация пользователя в Django
    login(request, user)

    # Перенаправление на главную страницу
    return redirect(reverse('main_page'))
