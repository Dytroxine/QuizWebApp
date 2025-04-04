# Generated by Django 5.1.3 on 2025-02-14 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_quiz_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.question', verbose_name='Вопрос'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer',
            name='text_answer',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Текстовый ответ'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.choice', verbose_name='Выбранный ответ'),
        ),
    ]
