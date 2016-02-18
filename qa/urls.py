from django.conf.urls import patterns, include, url

from qa.views import QuestionListView, QuestionView, QuestionNewView, \
    QuestionUpdateView, QuestionDeleteView, VoteView

urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name='questions'),
    url(r'^q/(?P<slug_title>[\w-]+)$', QuestionView.as_view(), name='question'),
    url(r'^new$', QuestionNewView.as_view(), name='new'),
    url(r'^edit/(?P<slug_title>[\w-]+)$', QuestionUpdateView.as_view(),
        name='edit'),
    url(r'^delete/(?P<slug_title>[\w-]+)$', QuestionDeleteView.as_view(),
        name='delete'),
    url(r'^vote/(?P<slug_title>[\w-]+)$', VoteView.as_view(),
        name='vote')
    # url(r'^vote/(.+)$', VoteView.as_view(), name='vote'),
]
