# Generated by Django 5.1.3 on 2025-02-14 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_question_correct_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoadingText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100, verbose_name='Текст под экраном загрузки')),
            ],
        ),
    ]
