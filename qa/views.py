from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from qa.models import Question, Answer, Comment
from qa.forms import QuestionNewForm

class QuestionListView(TemplateView):
    model = Question
    template_name = 'qa/questions.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        questions = Question.objects.select_related('user')
        paginator = Paginator(questions, 15)
        page = self.request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)
        context['questions'] = questions
        return context

class QuestionView(TemplateView):
    model = Question
    template_name = 'qa/question.html'

    def get_context_data(self, **kwargs):

        context = super(QuestionView, self).get_context_data(**kwargs)

        try:
            question = Question.objects \
                .select_related('user') \
                .prefetch_related('answers',
                                  'answers__user',
                                  'answers__comments',
                                  'answers__comments__user') \
                .get(slug_title=kwargs['slug_title'])

        except Question.DoesNotExist:
            raise Http404()

        context['question'] = question
        return context

class QuestionNewView(CreateView):
    model = Question
    template_name = 'qa/new.html'
    form_class = QuestionNewForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionNewView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse_lazy('question', obj.slug_title))