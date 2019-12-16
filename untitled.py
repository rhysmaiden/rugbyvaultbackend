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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match
from rugby.models import Team
from rugby.models import Player
from rugby.models import Try

def make_soup(url):

	thepage = urllib.request.urlopen(url)
	soupdata = BeautifulSoup(thepage, "html.parser")
	return soupdata

url = "https://www.bbc.com/sport/rugby-union/world-cup/scores-fixtures/2019-10?filter=result"
soup = make_soup(url)

len(soup.findAll('div', {'class': 'full-team-name'}))
