
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

import youtube_videos
from youtube_videos import youtube_search

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match
from rugby.models import Team
from rugby.models import Player
from rugby.models import Try
from rugby.models import League

matches = Match.objects.filter(league_id = League.objects.filter(name="Super Rugby")[0]).order_by("-date")

for match in matches:
    found_videos = youtube_search(match.video_link,DEVELOPER_KEY="AIzaSyDgSdNuzbho-hF1hjADW_OFpWlMp6J4img")

    print(found_videos)



