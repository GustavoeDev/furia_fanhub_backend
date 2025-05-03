from django.urls import path

from .views import ChatView, ChatMessageView

urlpatterns = [
    path('', ChatView.as_view()),
    path('<int:match_id>/', ChatView.as_view()),
    path('messages/<int:chat_id>/', ChatMessageView.as_view()),
]