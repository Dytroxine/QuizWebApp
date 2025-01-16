# Generated by Django 5.1.3 on 2024-11-18 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_alter_question_multipliers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='question_count',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='time_per_question',
            field=models.PositiveIntegerField(default=20, verbose_name='Время на вопрос (секунды)'),
        ),
    ]
