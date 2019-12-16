from pytube import YouTube
import os
import subprocess
import time
import datetime
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Match

time_period = datetime.today() - timedelta(days=7)
matches = Match.objects.filter(date__gte=time_period).filter(video_link_found=1).filter(video_downloaded=0)

for match in matches:

    if not os.path.exists('videos/' + str(match.id) + '.mp4'):
        yt = YouTube(match.video_link)
        yt.streams.first().download(output_path="videos/", filename=str(match.id))

        match.video_downloaded = 1
        match.save()
    else:
        print("Already downloaded")
        match.video_downloaded = 1
        match.save()
