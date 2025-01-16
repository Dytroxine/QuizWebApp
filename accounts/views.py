from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User


@csrf_exempt  # Отключаем проверку CSRF для запросов от бота
def bot_register(request):
    if request.method == 'POST':
        data = request.POST

        # Получение данных от бота
        telegram_id = data.get('telegram_id')
        username = data.get('username', f'telegram_user_{telegram_id}')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        # Проверка обязательных полей
        if not telegram_id:
            return JsonResponse({'error': 'Missing telegram_id'}, status=400)

        # Создание или обновление пользователя
        user, created = User.objects.get_or_create(telegram_id=telegram_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Возвращаем ответ для бота
        return JsonResponse({'status': 'success', 'created': created})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
