from rest_framework import serializers

from .models import Competition, Team

from django.conf import settings

class CompetitionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'end_date', 'location']

class TeamSerializer(serializers.ModelSerializer):
    competitions = CompetitionSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'competitions']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logo'] = f"{settings.CURRENT_URL}{instance.logo}"

        return data
    
class CompetitionSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'logo', 'teams', 'start_date', 'end_date', 'location']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logo'] = f"{settings.CURRENT_URL}{instance.logo}"

        return data
