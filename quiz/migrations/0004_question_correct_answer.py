# Generated by Django 5.1.3 on 2025-02-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_remove_question_is_multiple_choice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Правильный ответ'),
        ),
    ]
