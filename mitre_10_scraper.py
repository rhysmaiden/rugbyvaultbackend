#Run everday at 1pm

import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
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

for page_num in range(1, 20):
	

	url = "https://www.ultimaterugby.com/mitre-10-cup-2020/results?page=" + str(page_num)

	print(url)
	soup = make_soup(url)

	matches = soup.findAll('div', {'class': 'match-item'})
	
	for match_item in matches:
		match_date_item = match_item.find('meta', {'itemprop': 'startDate'})

		if match_date_item:
			date_string = match_date_item.get('content')[:10]
			date_formatted = datetime.strptime(date_string, '%Y-%m-%d')
		else:
			continue

		home_team_name = match_item.findAll('span', {'class': 'team-name'})[0].text
		away_team_name = match_item.findAll('span', {'class': 'team-name'})[1].text

		team_one_obj = Team.objects.filter(team_name=home_team_name)[0]
		team_two_obj = Team.objects.filter(team_name=away_team_name)[0]

		existing = Match.objects.filter(home_team=team_one_obj,away_team=team_two_obj).order_by('-date')

		if len(existing) > 0:
			if abs(existing[0].date - date_formatted) < timedelta(days=4):
				existing.update(region_blocked = match_item.find('meta', {'itemprop': 'url'}).get('content'))
				continue

		

		new_match = Match(home_team=team_one_obj, away_team=team_two_obj, date=date_formatted, home_score=0, away_score=0, league_id=team_one_obj.league_id)
		
		new_match.region_blocked = match_item.find('meta', {'itemprop': 'url'}).get('content')
		print(new_match)
		new_match.save()
	

	