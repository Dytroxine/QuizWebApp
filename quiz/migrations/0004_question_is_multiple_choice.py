# Generated by Django 5.1.3 on 2024-11-15 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz_time_per_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_multiple_choice',
            field=models.BooleanField(default=False, verbose_name='Множественный выбор'),
        ),
    ]
