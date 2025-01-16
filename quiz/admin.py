from django.contrib import admin
from quiz.models import Quiz, Question, Choice
from .forms import QuizForm
from django.db import models
from django.http import HttpResponse
from django.urls import path
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils.html import format_html
from django.shortcuts import redirect

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'show_activate_button')

    def show_activate_button(self, obj):
        if not obj.is_active:
            return format_html(
                '<a class="button" href="{}">Активировать</a>',
                f'{obj.id}/activate/'
            )
        return "Уже активирован"
    show_activate_button.short_description = "Действие"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:quiz_id>/activate/', self.admin_site.admin_view(self.activate_quiz), name='quiz-activate'),
        ]
        return custom_urls + urls

    def activate_quiz(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        if not quiz.is_active:
            quiz.is_active = True
            quiz.save()

            # Отправка WebSocket сообщения
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"quiz_{quiz_id}",
                {
                    "type": "start_quiz",  # Это связано с `start_quiz` в `QuizConsumer`
                    "quiz_id": quiz_id,
                }
            )

            self.message_user(request, f"Квиз '{quiz.title}' успешно активирован.")
        else:
            self.message_user(request, f"Квиз '{quiz.title}' уже активирован.", level='warning')
        return redirect(f'/admin/quiz/quiz/{quiz_id}/change/')





@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'time_limit', 'points')  # Отображение в списке
    list_filter = ('quiz',)  # Фильтры в боковой панели
    search_fields = ('text',)  # Поиск по тексту вопроса
    ordering = ('quiz', 'text')  # Сортировка по квизу и тексту вопроса

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')  # Отображение в списке
    list_filter = ('question', 'is_correct')  # Фильтры в боковой панели
    search_fields = ('text',)  # Поиск по тексту ответа
    ordering = ('question', 'text')  # Сортировка по вопросу и тексту ответа

