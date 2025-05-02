from django.urls import path
from .views import TeamView, CompetitionView, GenerateMatchesView, MatchesView

urlpatterns = [
    path('', CompetitionView.as_view()),
    path('<int:competition_id>/', CompetitionView.as_view()),
    path('<int:competition_id>/add-teams/', CompetitionView.as_view()),
    path('teams/', TeamView.as_view()),
    path('teams/<int:team_id>/', TeamView.as_view()),
    path('<int:competition_id>/generate-matches/', GenerateMatchesView.as_view()),
    path('<int:competition_id>/matches/<int:match_id>/', MatchesView.as_view()),
]