from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.socket import socket

from .models import Chat, ChatMessage
from .serializers import ChatSerializer, ChatMessageSerializer

class ChatView(APIView):
    def get(self, request, match_id=None):
        if match_id:
            chat = Chat.objects.filter(match_id=match_id).first()
            if not chat:
                return Response({
                    "error": "Chat não encontrado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ChatSerializer(chat)
            return Response(serializer.data)
        
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

class ChatMessageView(APIView):
    def get(self, request, chat_id):
        if not chat_id:
            return Response({
                "error": "ID do chat não fornecido"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        messages = ChatMessage.objects.filter(chat_id=chat_id)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request, chat_id):
        body = request.data.get('body')

        if not body:
            return Response({
                "error": "Corpo da mensagem não fornecido"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not chat_id:
            return Response({
                "error": "ID do chat não fornecido"
            }, status=status.HTTP_400_BAD_REQUEST)

        message = ChatMessage.objects.create(
            body=body,
            chat_id=chat_id,
            from_user_id=request.user.id
        )

        message_data = ChatMessageSerializer(message).data

        socket.emit('update_chat_message', {
            'message': message_data,
            'chat_id': chat_id,
        })

        return Response(message_data, status=status.HTTP_201_CREATED)
        

