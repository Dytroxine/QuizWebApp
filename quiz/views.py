from django.shortcuts import render, get_object_or_404
from quiz.models import Quiz, Choice, Answer, User, LoadingText, Question
from django.db import models
from math import ceil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count, Sum


def quiz_view(request, telegram_id):
    quiz = Quiz.objects.filter(is_displayed=True).first()
    loading_texts = list(LoadingText.objects.values_list('text', flat=True))
    user = User.objects.get(telegram_id=telegram_id)
    my_score = user.get_quiz_score()
    count = sum(1 for user in User.objects.all() if user.get_quiz_score() > my_score) + 1

    user_answers_count = Answer.objects.filter(
        user__telegram_id=telegram_id,  # Фильтрация по Telegram ID пользователя
        question__quiz=quiz  # Фильтрация по викторине (учитывает и choice, и text_answer)
    ).values('question').distinct().count()
    if quiz:
        total_time_in_seconds = quiz.questions.aggregate(
            total_time=models.Sum('time_limit')
        )['total_time'] or 0
        duration_in_minutes = ceil(total_time_in_seconds / 60)
        quiz.duration_in_minutes = duration_in_minutes

    return render(request, 'quiz/home.html', {'quiz': quiz, 'user_answers_count': user_answers_count, 'telegram_id':
        telegram_id, 'loadingTexts': loading_texts, 'user_place': count,
                                              'promocode': quiz.reward.promocode})


@csrf_exempt
def submit_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            choice_id = data.get('choice_id', None)  # Может быть None
            text_answer = data.get('text_answer', None)  # Может быть None
            question_id = data.get('question_id', None)  # Может быть None

            user = User.objects.filter(telegram_id=telegram_id).first()
            if not user:
                return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'}, status=404)

            if choice_id:
                choice = Choice.objects.filter(id=choice_id).first()
                if not choice:
                    return JsonResponse({'status': 'error', 'message': 'Выбранный вариант не найден'}, status=404)

                Answer.objects.create(user=user, choice=choice, question=choice.question)

            elif text_answer and question_id:
                question = Question.objects.filter(id=question_id).first()
                if not question:
                    return JsonResponse({'status': 'error', 'message': 'Вопрос не найден'}, status=404)

                # Проверяем, отвечал ли пользователь на этот текстовый вопрос
                existing_answer = Answer.objects.filter(user=user, question=question).first()
                if existing_answer:
                    return JsonResponse({'status': 'error', 'message': 'Вы уже отвечали на этот вопрос'}, status=400)

                # Если ответа нет, создаем новый
                Answer.objects.create(user=user, text_answer=text_answer, question=question)

            else:
                return JsonResponse({'status': 'error', 'message': 'Недостаточно данных'}, status=400)

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Ошибка в JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Неверный метод'}, status=405)
