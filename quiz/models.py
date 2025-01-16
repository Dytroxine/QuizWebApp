from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Quiz(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название квиза")
    banner = models.ImageField(upload_to='quiz_banners/', verbose_name="Баннер")
    is_active = models.BooleanField(default=False, verbose_name="Активен")
    is_displayed = models.BooleanField(default=False, verbose_name="Отображать на главной странице")

    @property
    def question_count(self):
        return self.questions.count()  # Связанные вопросы через related_name

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Вопрос")
    text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    time_limit = models.PositiveIntegerField(default=20, verbose_name="Время на ответ (секунды)")
    points = models.PositiveIntegerField(default=1, verbose_name="Очки за ответ")
    multipliers = models.JSONField(verbose_name="Множители",  default=dict)
    is_multiple_choice = models.BooleanField(verbose_name="Множественный выбор", default=False)

    def __str__(self):
        return f"{self.quiz.title}: {self.text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choice", verbose_name="Ответ")
    text = models.CharField(max_length=100, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный вариант")

    def __str__(self):
        return f"{self.question.text}: {self.text}"


