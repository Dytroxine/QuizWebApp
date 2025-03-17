from django.contrib import admin
from django.urls import path
from quiz import views

app_name = 'quiz'


urlpatterns = [
    path('<int:telegram_id>/', views.quiz_view, name='quiz_view'),
    path('submit_answer/', views.submit_answer, name='submit_answer')

]