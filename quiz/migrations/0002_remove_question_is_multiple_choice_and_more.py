# Generated by Django 5.1.3 on 2024-11-15 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='is_multiple_choice',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='time_per_question',
        ),
        migrations.AddField(
            model_name='question',
            name='multipliers',
            field=models.JSONField(default=dict, verbose_name='Множители'),
        ),
        migrations.AddField(
            model_name='question',
            name='points',
            field=models.PositiveIntegerField(default=1, verbose_name='Очки за ответ'),
        ),
        migrations.AddField(
            model_name='question',
            name='time_limit',
            field=models.PositiveIntegerField(default=60, verbose_name='Время на ответ (секунды)'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='banner',
            field=models.ImageField(default=1, upload_to='quiz_banners/', verbose_name='Баннер'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активен'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='is_displayed',
            field=models.BooleanField(default=False, verbose_name='Отображать на главной странице'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='question_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество вопросов'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='Правильный вариант'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice', to='quiz.question', verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=100, verbose_name='Текст ответа'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=200, verbose_name='Текст вопроса'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название квиза'),
        ),
    ]
