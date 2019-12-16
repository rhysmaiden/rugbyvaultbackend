from pytube import YouTube
import os
import subprocess
import time
import datetime


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

time_period = datetime.today() - timedelta(days=7)
matches = Match.objects.filter(date__gte=time_period).filter(video_link_found=1).filter(video_downloaded=0)

for match in matches:
    tries = Try.objects.filter(match=match).order_by(minute)
    print(tries)


yt = YouTube("https://www.youtube.com/watch?v=n06H7OcPd-g")
yt = yt.get('mp4', '720p')
yt.download('/path/to/download/directory')
