#Run everday at 1pm

import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
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



def check_for_alternate_name(team_name):
	
	for team in alternate_names:
		if team["espn_name"] == team_name:
			team_name = team["vault_name"]
			
			return team_name

	return team_name


def make_soup(url):

	thepage = urllib.request.urlopen(url)
	soupdata = BeautifulSoup(thepage, "html.parser")
	return soupdata

for i in range(0,10000):

	try:

		date = datetime.today() - timedelta(days=i)
		print(date)
		url_date = date.strftime('%Y%m%d')


		url = "https://www.espn.com.au/rugby/fixtures/_/date/" + url_date
		soup = make_soup(url)

		

		a_teams = soup.findAll('td', {'class': 'team-a'})
		b_teams = soup.findAll('td', {'class': 'team-b'})


		for a,b in zip(a_teams,b_teams):
			team_one = a.find('abbr').get('title')
			team_two = b.find('abbr').get('title')

			team_one = check_for_alternate_name(team_one)
			team_two = check_for_alternate_name(team_two)

		

			try:

				team_one_obj = Team.objects.filter(team_name=team_one)[0]
				team_two_obj = Team.objects.filter(team_name=team_two)[0]



			except:
				print("FAILED: ",team_one,team_two)
				continue




			existing = Match.objects.filter(home_team=team_one_obj,away_team=team_two_obj).order_by('-date')

			if len(existing) > 0:
				if abs(existing[0].date - date) < timedelta(days=4):
					#print("EXISTS: ",team_one,team_two)
					continue

			print("NEW: ",team_one,team_two)

			new_match = Match(home_team=team_one_obj,away_team=team_two_obj,date=date,home_score=0,away_score=0,league_id=team_one_obj.league_id)
			new_match.save()
	except:
		print("Page failed")


