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
from youtube_search import YoutubeSearch
import json
# from youtube_search_v2 import search

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match

matches = Match.objects.all()

for m in matches:
    if "embed" in m.video_link:
        split = m.video_link.split("/")
        # print(split[-1])
        m.video_link = "https://www.youtube.com/watch?v=" + split[-1]
        m.error = 0
        m.save()

        # https://www.youtube.com/watch?v=QXokTpJGduw
        # https://www.youtube.com/embed/PUURKeAZNyQ