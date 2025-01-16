from django.contrib import admin
from django.urls import path
from quiz import views

app_name = 'quiz'


urlpatterns = [
    path('<int:quiz_id>/', views.quiz_view, name='quiz_view'),
]