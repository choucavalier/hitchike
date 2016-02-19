from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db.models import Count
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from qa.models import Question, Answer, Comment
from qa.forms import QuestionForm, AnswerForm

class QuestionListView(TemplateView):
    model = Question
    template_name = 'qa/questions.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        questions = Question.objects \
            .annotate(answers_count=Count('answers')) \
            .select_related('user')
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

        hit_count = HitCount.objects.get_for_object(question)
        HitCountMixin.hit_count(self.request, hit_count)

        if self.request.user.is_authenticated():
            context['user_voted'] = not question.votes.exists(self.request.user)
        else:
            context['user_voted'] = False

        context['question'] = question
        return context

class AnswerNewView(CreateView):
    model = Answer
    template_name = 'qa/answer.html'
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        context = super(AnswerNewView, self).get_context_data(**kwargs)
        context['question'] = self.question
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
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
        self.question = question
        return super(AnswerNewView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        form.save_m2m()
        self.question.answers.add(obj)
        return HttpResponseRedirect(reverse_lazy('qa:question', kwargs={
            'slug_title': self.question.slug_title}))

class QuestionNewView(CreateView):
    model = Question
    template_name = 'qa/new.html'
    form_class = QuestionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionNewView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse_lazy('qa:question', kwargs={
            'slug_title': obj.slug_title}))

class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'qa/edit.html'
    form_class = QuestionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = Question.objects.get(slug_title=self.kwargs['slug_title'])
        return obj

    def get_success_url(self):
        return reverse_lazy('qa:question',
                kwargs={'slug_title': self.object.slug_title})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse_lazy('qa:question', kwargs={
            'slug_title': obj.slug_title}))

class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('qa:questions')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = Question.objects.get(user=self.request.user,
                                   slug_title=self.kwargs['slug_title'])
        return obj



@login_required
def vote_question(request, **kwargs):
    try:
        question = Question.objects.\
            get(slug_title=kwargs['slug_title'])
    except Question.DoesNotExist:
        raise Http404()

    user = request.user
    if question.user != user:
        if question.votes.exists(user):
            question.votes.down(user)
        else:
            question.votes.up(user)
    else:
        return HttpResponse(-1)
    return HttpResponse(question.votes.count())