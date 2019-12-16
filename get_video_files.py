
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
from random import randint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match
from rugby.models import Team
from rugby.models import Player
from rugby.models import Try
from rugby.models import League


team = Team.objects.filter(team_name="Australia")[0]
tries = Try.objects.filter(team=team,match__date__year='2019').order_by('-match__date')

i = 0

for t in tries:
	i+=1

	url = t.match.video_link
	length = t.end_time - t.start_time
	start_time = t.start_time
	name = "Australia2019/" + str(i) + (str(t) + ".mkv").replace('-','').replace(' ','')

	command = "ffmpeg $(youtube-dl -g " + url + ' | sed "s/.*/-ss ' + str(start_time) + ' -i &/") -t ' + str(length) + ' -c copy ' + name
	#print(command)
	os.system(command)

os.system('for i in Australia2019/*.mkv; do ffmpeg -i "$i" -codec copy -strict -2 "${i%.*}.mp4"; done')




	