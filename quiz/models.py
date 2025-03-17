from django.db import models
from django.conf import settings
from django.utils.timezone import now


class User(models.Model):
    telegram_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.telegram_id}"

    def get_quiz_score(self):
        """Возвращает количество баллов пользователя в квизе с `is_displayed=True`."""
        from .models import Quiz, Answer, Choice, Question  # Импорт внутри метода, чтобы избежать циклических импортов

        # Находим активный квиз с `is_displayed=True`
        quiz = Quiz.objects.filter(is_displayed=True).first()
        if not quiz:
            return 0  # Если нет активного квиза, баллы 0

        user_answers = Answer.objects.filter(user=self, question__quiz=quiz)

        total_score = 0
        for question in quiz.questions.all():
            if question.question_type == 'text_input':
                # Получаем ответ пользователя для текстового вопроса
                user_text_answer = user_answers.filter(question=question).values_list("text_answer", flat=True).first()

                # Проверяем, что текстовый ответ совпадает с правильным
                if user_text_answer and user_text_answer.strip().lower() == question.correct_answer.strip().lower():
                    total_score += 1

            else:
                correct_choices = set(
                    question.choice.filter(is_correct=True).values_list("id", flat=True))  # ID всех правильных ответов
                user_choices = set(
                    user_answers.filter(question=question).values_list("choice__id",
                                                                       flat=True))  # ID ответов пользователя

                # Проверяем, что все правильные выбраны и нет лишних
                if correct_choices and correct_choices == user_choices:
                    total_score += 1  # 1 балл за правильно решенный вопрос

        return total_score


class Promocodes(models.Model):
    promocode = models.CharField(max_length=100, verbose_name="Промокод")
    is_given = models.BooleanField(default=False, verbose_name="Выдан ли пользователю")
    user = models.ForeignKey(User, blank=True, null=True, default=None,  on_delete=models.CASCADE, related_name="winner", verbose_name="Получатель")

    def __str__(self):
        if self.is_given and self.user:
            return f"Промокод: {self.promocode} | Выдан: {self.user.username}"
        return f"Промокод: {self.promocode} | Не выдан"


class Quiz(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название квиза")
    banner = models.ImageField(upload_to='quiz_banners/', verbose_name="Баннер")
    is_active = models.BooleanField(default=False, verbose_name="Активен")
    is_displayed = models.BooleanField(default=False, verbose_name="Отображать на главной странице")
    reward = models.ForeignKey(Promocodes, blank=True, null=True, default=None, on_delete=models.CASCADE, related_name="promocodes", verbose_name="награда")

    @property
    def question_count(self):
        return self.questions.count()  # Связанные вопросы через related_name

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = (
        ('single_choice', 'Одиночный выбор'),
        ('multiple_choice', 'Множественный выбор'),
        ('text_input', 'Ввод текста'),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Вопрос")
    text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    time_limit = models.PositiveIntegerField(default=20, verbose_name="Время на ответ (секунды)")
    points = models.PositiveIntegerField(default=1, verbose_name="Очки за ответ")
    multipliers = models.JSONField(verbose_name="Множители",  default=dict)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Тип вопроса",
                                     default="single_choice")
    correct_answer = models.CharField(max_length=500, verbose_name="Правильный ответ", blank=True, null=True)


    def __str__(self):
        return f"{self.quiz.title}: {self.text} ({self.get_question_type_display()})"

    def save(self, *args, **kwargs):
        """
        Убираем correct_answer, если вопрос не text_input
        """
        if self.question_type != 'text_input':
            self.correct_answer = None  # Очищаем поле, если это не текстовый ввод
        super().save(*args, **kwargs)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choice", verbose_name="Ответ")
    text = models.CharField(max_length=100, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный вариант")

    def __str__(self):
        return f"{self.question.text}: {self.text}"





class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answerer", verbose_name="Пользователь")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answers", verbose_name="Выбранный ответ",
                               null=True, blank=True)
    text_answer = models.CharField(max_length=500, verbose_name="Текстовый ответ", null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers",
                                 verbose_name="Вопрос")  # Привязка к вопросу

    def __str__(self):
        if self.choice:
            return f"{self.user.telegram_id} выбрал: {self.choice.text}"
        return f"{self.user.telegram_id} ответил текстом: {self.text_answer}"


class LoadingText(models.Model):
    text = models.CharField(max_length=100, verbose_name="Текст под экраном загрузки")

    def __str__(self):
        return f"{self.text}"




