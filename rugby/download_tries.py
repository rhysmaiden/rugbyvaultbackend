import django
import wikipedia
import os
import subprocess
import youtube_videos
import time
import datetime
from datetime import datetime, timedelta

import json
# from youtube_search_v2 import search

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match

import youtube_dl, subprocess

URL = "https://www.youtube.com/watch?v=eyU3bRy2x44"
FROM = "00:00:15"
TO = "00:00:25"
TARGET = "demo.mp4"

with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
    result = ydl.extract_info(URL, download=False)
    video = result['entries'][0] if 'entries' in result else result

url = video['url']
subprocess.call('ffmpeg -i "%s" -ss %s -t %s -c:v copy -c:a copy "%s"' % (url, FROM, TO, TARGET))