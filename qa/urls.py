from django.conf.urls import patterns, include, url

from qa.views import QuestionListView, QuestionView, QuestionNewView

urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name='questions'),
    url(r'^q/(?P<slug_title>[\w-]+)$', QuestionView.as_view(), name='question'),
    url(r'^new$', QuestionNewView.as_view(), name='new'),
    # url(r'^edit/(.+)$', EditQuestionView.as_view(), name='edit'),
    # url(r'^vote/(.+)$', VoteView.as_view(), name='vote'),
]