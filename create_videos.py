
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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match
from rugby.models import Team
from rugby.models import Player
from rugby.models import Try
from rugby.models import League

team = Team.objects.filter(team_name="Australia")[0]

tries = Try.objects.filter(team=team,match__date__year='2019').order_by('-match__date')

table = "**" + "Tries by Australia in 2019" + "**\n\n"
table += "|Match|Player|Video Link|\n|:--|:--|--:|"
i = 0
for t in tries:
    i+=1

    table += "\n" + str(i) + ". " + str(t.match.home_team.team_name) + " vs " + str(t.match.away_team.team_name) + " : " + t.player.name + " | " + t.video_link + ""

print(table)
