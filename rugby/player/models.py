from django.db import models

from rugby.team.models import Team
from rugby.trie.models import Trie
from rugby.league.models import League

class Player(models.Model):
    name = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    internation_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='h', default=2)

    def __str__(self):
        return self.name + ' - ' + self.team.team_name

    def number_of_tries(self):
        tries = Trie.objects.filter(player=self)
        return len(tries)

    def number_of_int_tries(self):
        tries = Trie.objects.filter(player=self,match__league_id=League.objects.filter(name="International")[0])
        return len(tries)