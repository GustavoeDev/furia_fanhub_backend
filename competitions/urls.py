from django.urls import path
from .views import TeamView, CompetitionView, GenerateMatchesView

urlpatterns = [
    path('', CompetitionView.as_view()),
    path('<int:competition_id>/', CompetitionView.as_view()),
    path('<int:competition_id>/add-teams/', CompetitionView.as_view()),
    path('teams/', TeamView.as_view()),
    path('teams/<int:team_id>/', TeamView.as_view()),
    path('generate-matches/<int:competition_id>/', GenerateMatchesView.as_view()),
]