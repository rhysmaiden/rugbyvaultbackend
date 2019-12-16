import wikipedia
import os
import subprocess
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Player

players = Player.objects.all()

x=0

for p in players:
    x+=1

    print(p.name)
