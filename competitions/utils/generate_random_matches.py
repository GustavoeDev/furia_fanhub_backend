from itertools import combinations
from datetime import datetime, timedelta
from competitions.models import Match, Competition
import random

from chats.models import Chat

def generate_real_matches(competition_id):
    competition = Competition.objects.get(id=competition_id)

    teams = competition.teams.all()

    matchups = combinations(teams, 2)  

    matches = []
    
    total_rounds = 24  

    for team_1, team_2 in matchups:
        start_time = datetime.now() + timedelta(days=random.randint(1, 30))

        match = Match.objects.create(
            competition=competition,
            team_1=team_1,
            team_2=team_2,
            round_number=total_rounds,  
            map_played=random.choice(['mirage', 'inferno', 'nuke', 'overpass', 'dust_2', 'train', 'vertigo', 'ancient']),  
            start_time=start_time,
            status='pending' 
        )

        Chat.objects.create(
            match=match,
        )

        matches.append(match)

    return matches
