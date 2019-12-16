import wikipedia
import os
import subprocess
from datetime import datetime, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Match

time_period = datetime.today() - timedelta(days=10)

matches = Match.objects.filter(date__gte=time_period).filter(video_link_found=0)

for match in matches:
    print(match)
