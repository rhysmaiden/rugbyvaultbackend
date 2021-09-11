from django.db import models

from rugby.team.models import Team
from rugby.league.models import League
from rugby.rating.models import UserRating

from rugby.choices import MatchErrorChoices

class MatchBase(models.Model):
    date = models.DateTimeField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='%(class)s_home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='%(class)s_away_team')
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date.date()) + '-' + str(self.home_team.team_name) + " vs " + str(self.away_team.team_name)

    class Meta:
        abstract = True

class ScrapedMatch(MatchBase):
    pass

class Match(MatchBase):
    video_link = models.TextField()
    is_processed = models.BooleanField()

class ErrorMatch(MatchBase):
    error = models.IntegerField(choices=MatchErrorChoices.CHOICES)

class MatchRating(UserRating):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)