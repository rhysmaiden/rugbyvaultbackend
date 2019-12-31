# Run script every 3 hours



import django
import wikipedia
import os
import subprocess
import youtube_videos
import time
import datetime
from youtube_videos import youtube_search
from datetime import datetime, timedelta
# from youtube_search_v2 import search

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match
from rugby.models import Try


names = []

tries = Try.objects.filter(match__date__year="2018")

for index,t in enumerate(tries):
    if not any(d['name'] == t.player.name for d in names):
        new_player = {'name':t.player.name,'tries':1}
        names.append(new_player)
    else:
        for n in names:
            if n['name'] == t.player.name:
                n['tries'] = n['tries'] + 1
                break

playerlist = sorted(names, key=lambda k: k['tries'])

print(playerlist)