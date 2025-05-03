from django.db import models

from competitions.models import Match
from accounts.models import User

class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='chats')

    class Meta:
        db_table = 'chats'

class ChatMessage(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
