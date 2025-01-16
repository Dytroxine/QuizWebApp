from django.shortcuts import render, get_object_or_404
from quiz.models import Quiz
from django.db import models
from math import ceil
from django.http import JsonResponse


def quiz_view(request, quiz_id):
    quiz = Quiz.objects.filter(is_displayed=True).first()
    if quiz:
        total_time_in_seconds = quiz.questions.aggregate(
            total_time=models.Sum('time_limit')
        )['total_time'] or 0
        duration_in_minutes = ceil(total_time_in_seconds / 60)
        quiz.duration_in_minutes = duration_in_minutes

    return render(request, 'quiz/home.html', {'quiz': quiz})



def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save()
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'form': form})


def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form, 'quiz': quiz})


def add_choice_options(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = ChoiceForm()
    return render(request, 'quiz/add_choices.html', {'form': form, 'question': question})
