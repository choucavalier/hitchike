from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from hitcount.models import HitCountMixin
from taggit.managers import TaggableManager
from vote.managers import VotableManager

from qa.render import render

class BaseModel(models.Model):
    user = models.ForeignKey(User)
    create_at = models.DateTimeField(auto_now_add=True)
    votes = VotableManager()
    content_html = models.TextField(blank=True, editable=False)
    content = models.TextField()

    def save(self, *args, **kwargs):
        self.content_html = render(self.content)
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Comment(BaseModel):

    class Meta(BaseModel.Meta):
        ordering = ['create_at']

class Answer(BaseModel):
    comments = models.ManyToManyField(Comment, related_name='answer_comments')
    validated = models.BooleanField(default=False)

class Question(BaseModel, HitCountMixin):
    title = models.CharField('Question', max_length=140)
    slug_title = models.SlugField(max_length=140, unique=True)
    tags = TaggableManager()
    answers = models.ManyToManyField(Answer, related_name='question_answers')
    answered = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate slug_title if this is a newly created question
        if not self.pk:
            self.slug_title = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        ordering = ['-create_at']
