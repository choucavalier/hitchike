from django import forms

from pagedown.widgets import PagedownWidget

from qa.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
                'title',
                'tags',
                'content',
                ]
        widgets = {
            'content': PagedownWidget(attrs={}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': PagedownWidget(attrs={}),
        }
