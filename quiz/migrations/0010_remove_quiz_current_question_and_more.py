# Generated by Django 5.1.3 on 2025-01-15 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_quiz_current_question_quiz_timer_end_time_quizanswer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='current_question',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='timer_end_time',
        ),
        migrations.DeleteModel(
            name='QuizAnswer',
        ),
    ]
