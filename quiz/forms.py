from django import forms
from .models import Quiz, Question, Choice

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'time_limit', 'points', 'multipliers']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Текст вопроса'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'multipliers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '{"1": 2, "2": 1.7, ...}'})
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Текст ответа'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
