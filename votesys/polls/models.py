import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField("date published")
  share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

  def __str__(self):
    return self.question_text
  
  @admin.display(
    boolean=True,
    ordering="pub_date",
    description="Published recently?",
  )
  
  def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
  # we use many-one relationship (many choice has only one question)
  # the on_delete is used for safety instruction if question not there no choices
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.choice_text
  
class Comment(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.username} on {self.question}"

REACTION_CHOICES = [
  ('interesting', '👍 Interesting'),
  ('controversial', '🔥 Controversial'),
  ('funny', '😂 Funny'),
  ('important', '❗ Important'),
]

class Reaction(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reactions')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)

  class Meta:
    unique_together = ('question', 'user')  # one reaction per user per poll

  def __str__(self):
    return f"{self.user.username} reacted {self.reaction_type} to '{self.question}'"

