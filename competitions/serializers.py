from rest_framework import serializers

from .models import Competition, Team, Match

from django.conf import settings
from django.db.models import Q

class CompetitionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'end_date', 'location']

class TeamSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'logo']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'competition', 'team_1', 'team_2', 'score_team_1', 'score_team_2', 'map_played', 'round_number', 'start_time', 'end_time', 'status']

class TeamSerializer(serializers.ModelSerializer):
    competitions = CompetitionSimpleSerializer(many=True, read_only=True)
    matches = serializers.SerializerMethodField()

    def get_matches(self, team):
        matches = Match.objects.filter(Q(team_1=team) | Q(team_2=team))
        return MatchSerializer(matches, many=True).data

    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'competitions', 'matches']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logo'] = f"{settings.CURRENT_URL}{instance.logo}"

        return data
    
class CompetitionSerializer(serializers.ModelSerializer):
    teams = TeamSimpleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'logo', 'teams', 'start_date', 'end_date', 'location']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logo'] = f"{settings.CURRENT_URL}{instance.logo}"

        return data
