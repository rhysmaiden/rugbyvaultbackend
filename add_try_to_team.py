
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import wikipedia
import os
import subprocess
import django
import re
import difflib
from operator import itemgetter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match
from rugby.models import Team
from rugby.models import Player
from rugby.models import Try
from rugby.models import League

# team = Team.objects.filter(team_name="Australia")[0]

# tries = Try.objects.filter(team=team,match__date__year='2019').order_by('-match__date')

# table = "**" + "Tries by Australia in 2019" + "**\n"
# table += "|Match|Player|Video Link|\n:--|:--|"

# for t in tries:
#     table += "\n|" + str(t.match) + "|" + t.player.name + "|" + t.video_link

# print(table)

# players = []
# players_tuple = []

# tries = Try.objects.all()

# for t in tries:
#     player_name = t.player.name

#     if player_name in players:
#         for p in players_tuple:
#             if p[0] == player_name:
#                 p[1] += 1
#                 break
#     else:
#         players.append(player_name)
#         players_tuple.append([player_name,1])

# print(sorted(players_tuple,key=itemgetter(1)))


league_int=League.objects.filter(name="International")[0]

# tries = Try.objects.filter(team__league_id=league_int,match__date__range=[datetime.strptime("09-19-2019",'%m-%d-%Y'),datetime.today()]).order_by('match__date')

# table = "**" + "RWC 2019 Tries" + "**\n"
# table += "|Player|Match|Video Link|Player Profile\n:--|:--|"

# for t in tries:
#     table += "\n|" + t.player.name + "|" + t.match.home_team.team_name + " vs " + t.match.away_team.team_name + "|" + t.video_link + "|" + "https://www.therugbyvault.com/player/" + str(t.player.id)

# print(table)

matches = Match.objects.filter(league_id=league_int,date__range=[datetime.strptime("09-19-2019",'%m-%d-%Y'),datetime.today()]).order_by('date')

for m in matches:
    print(m)

