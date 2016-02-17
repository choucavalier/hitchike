from django import forms

from pagedown.widgets import PagedownWidget

from qa.models import Question

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
