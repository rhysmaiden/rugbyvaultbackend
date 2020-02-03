# Run script every 3 hours



import django
import wikipedia
import os
import subprocess

# from youtube_search_v2 import search

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match
from rugby.models import League

league = League.objects.filter(name="USA")[0]


Match.objects.filter(league_id=league).update(match_completely_processed=1)