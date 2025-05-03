from rest_framework import serializers
from .models import Chat, ChatMessage

from accounts.serializers import UserSerializer
from competitions.serializers import MatchSerializer

class ChatSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'created_at', 'finished_at', 'match']

class ChatMessageSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'body', 'created_at', 'chat', 'from_user']