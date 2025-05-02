from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.TextField()

    class Meta:
        db_table = 'teams'

class Competition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.TextField()
    teams = models.ManyToManyField(Team, related_name='competitions')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'competitions'

class Match(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('ongoing', 'Em andamento'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada'),
    ]

    MAP_CHOICES = [
        ('mirage', 'Mirage'),
        ('train', 'Train'),
        ('dust_2', 'Dust 2'),
        ('overpass', 'Overpass'),
        ('inferno', 'Inferno'),
        ('nuke', 'Nuke'),
        ('vertigo', 'Vertigo'),
        ('ancient', 'Ancient'),
    ]
    
    competition = models.ForeignKey(Competition, related_name='matches', on_delete=models.CASCADE)
    team_1 = models.ForeignKey(Team, related_name='matches_team_1', on_delete=models.CASCADE)
    team_2 = models.ForeignKey(Team, related_name='matches_team_2', on_delete=models.CASCADE)
    score_team_1 = models.IntegerField(default=0)
    score_team_2 = models.IntegerField(default=0)
    map_played = models.CharField(max_length=50, choices=MAP_CHOICES)  
    round_number = models.IntegerField(blank=True, null=True)  
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    @property
    def winner(self):
        if self.status != 'completed':
            return None
        if self.score_team_1 > self.score_team_2:
            return self.team_1
        elif self.score_team_2 > self.score_team_1:
            return self.team_2
        else:
            return "Empate"
    
    class Meta:
        db_table = 'matches'
        ordering = ['start_time'] 
    