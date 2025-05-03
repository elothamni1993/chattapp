from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}...'

# == chat/forms.py ==
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']