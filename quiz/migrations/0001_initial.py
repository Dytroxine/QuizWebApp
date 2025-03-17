# Generated by Django 5.1.3 on 2025-01-29 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Текст вопроса')),
                ('time_limit', models.PositiveIntegerField(default=20, verbose_name='Время на ответ (секунды)')),
                ('points', models.PositiveIntegerField(default=1, verbose_name='Очки за ответ')),
                ('multipliers', models.JSONField(default=dict, verbose_name='Множители')),
                ('is_multiple_choice', models.BooleanField(default=False, verbose_name='Множественный выбор')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название квиза')),
                ('banner', models.ImageField(upload_to='quiz_banners/', verbose_name='Баннер')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен')),
                ('is_displayed', models.BooleanField(default=False, verbose_name='Отображать на главной странице')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'quiz_user',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100, verbose_name='Текст ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный вариант')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice', to='quiz.question', verbose_name='Ответ')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz', verbose_name='Вопрос'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='quiz.choice', verbose_name='Ответ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answerer', to='quiz.user', verbose_name='Пользователь')),
            ],
        ),
    ]
