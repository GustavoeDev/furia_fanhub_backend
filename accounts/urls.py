from django.urls import path

from .views import UserSignInView, UserSignUpView, UserView

urlpatterns = [
   path('signin/', UserSignInView.as_view()),
   path('signup/', UserSignUpView.as_view()),
   path('me/', UserView.as_view()),
]