from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.utils import timezone

from django.core.files.storage import FileSystemStorage
from django.conf import settings

from competitions.serializers import MatchSerializer, TeamSerializer, CompetitionSerializer
from .utils.generate_random_matches import generate_real_matches 
from core.utils.exceptions import ValidationError

from .models import Competition, Match, Team

import uuid

class TeamView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return []
    
    def get(self, request, team_id=None):
        if team_id:
            team_id = int(team_id)
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                raise ValidationError("Time não encontrado.")
            serializer = TeamSerializer(team)
            return Response(serializer.data)
        
        else:
            teams = Team.objects.all()
            
            serializer = TeamSerializer(teams, many=True)

            return Response(serializer.data)
    
    def post(self, request):
        name = request.data.get('name')
        logo = request.FILES.get('logo')

        data = {
            'logo': logo,
            'name': name,
        }

        if not name or not logo:
            raise ValidationError('Campos obrigatórios não preenchidos.')

        if logo:
            content_type = logo.content_type
            extension = logo.name.split('.')[-1].lower() 

            if content_type not in ['image/jpeg', 'image/png'] or extension not in ['jpg', 'jpeg', 'png']:
                raise ValidationError('Suportamos apenas imagens JPEG e PNG')
            
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / 'teams',
                settings.MEDIA_URL + 'teams'
            )
            
            filename = f'{uuid.uuid4()}.{extension}'
            file = storage.save(filename, logo)
            logo_url = storage.url(file)
            data['logo'] = logo_url

        serializer = TeamSerializer(data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class CompetitionView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminUser()]
        return []

    def get(self, request):
        competitions = Competition.objects.all()
        
        serializer = CompetitionSerializer(competitions, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        name = request.data.get('name')
        logo = request.FILES.get('logo')
        teams = request.data.get('teams', [])
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        location = request.data.get('location')

        data = {
            'logo': logo,
            'name': name,
            'teams': teams,
            'start_date': start_date,
            'end_date': end_date,
            'location': location,
        }

        if not name or not logo or not location:
            raise ValidationError('Campos obrigatórios não preenchidos.')
        
        if logo:
            content_type = logo.content_type
            extension = logo.name.split('.')[-1].lower() 

            if content_type not in ['image/jpeg', 'image/png'] or extension not in ['jpg', 'jpeg', 'png']:
                raise ValidationError('Suportamos apenas imagens JPEG e PNG')
            
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / 'competitions',
                settings.MEDIA_URL + 'competitions'
            )
            
            filename = f'{uuid.uuid4()}.{extension}'
            file = storage.save(filename, logo)
            logo_url = storage.url(file)
            data['logo'] = logo_url

        serializer = CompetitionSerializer(data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
    def delete(self, request, competition_id):
        competition_id = int(competition_id)

        competition = Competition.objects.filter(id=competition_id).first()

        if not competition:
            raise ValidationError('Competição não encontrada.')
        
        competition.delete()
        return Response(status=204)
    
    def put(self, request, competition_id):
        teams = request.data.get('teams', [])

        if not isinstance(teams, list):
            raise ValidationError("Forneça uma lista de IDs de times válida.")

        try:
            competition = Competition.objects.get(id=competition_id)
        except Competition.DoesNotExist:
            raise ValidationError("Competição não encontrada.")

        valid_teams = Team.objects.filter(id__in=teams)
        
        if len(valid_teams) != len(teams):
            raise ValidationError("Alguns times fornecidos não foram encontrados.")

        competition.teams.set(valid_teams)
        competition.save()

        return Response({
            "message": "Lista de times atualizada com sucesso."
        })
    
class MatchesView(APIView):
    def get(self, request, competition_id, match_id=None):
        if match_id:
            match_id = int(match_id)
            try:
                match = Match.objects.get(id=match_id)
                
                now = timezone.now()
                
                if match.start_time and not match.end_time:
                    if match.start_time <= now and match.status != 'ongoing':
                        match.status = 'ongoing'
                        match.save()
                elif match.end_time and match.status != 'completed':
                        match.status = 'completed'
                        match.save()

            except Match.DoesNotExist:
                raise ValidationError("Partida não encontrada.")
            
            serializer = MatchSerializer(match)
            return Response(serializer.data)
        
        else:
            competition = Competition.objects.filter(id=competition_id).first()

            if not competition:
                raise ValidationError('Competição não encontrada.')

            matches = Match.objects.all().filter(competition=competition)

            if not matches:
                raise ValidationError('Essa competição não tem partidas.')
            
            serializer = MatchSerializer(matches, many=True)
            return Response(serializer.data)
    
class GenerateMatchesView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return []
    
    def post(self, request, competition_id):
        competition_id = request.data.get('competition_id')

        if not competition_id:
            return Response({
                'error': 'Você deve fornecer o ID da competição.'
            }, status=400)

        generate_real_matches(int(competition_id))

        return Response({
            'message': 'Partidas geradas com sucesso!'
        })