from django import forms

from qa.models import Question

class QuestionNewForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
                'title',
                'tags',
                'content',
                ]
