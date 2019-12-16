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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match

matches = Match.objects.all()

for idm, match in enumerate(matches):
    for idn, n in enumerate(matches):
        if idm == idn:
            continue



        if (match.date.day == n.date.day) and (match.date.month == n.date.month) and (match.date.year == n.date.year):
            if match.home_team == n.home_team:
                print(match)

                if match.video_link != "":
                    
                    if match.video_link == n.video_link:
                        print("MATCH")
                        n.delete()
                    else:
                        print(match.video_link)
                else:
                    print("X")
                    n.delete()
