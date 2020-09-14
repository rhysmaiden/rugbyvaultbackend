#Run everday at 1pm

import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import requests
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

alternate_names = [{
	"espn_name":"Gloucester Rugby",
	"vault_name":"Gloucester"
}, {
	"espn_name":"Bath Rugby",
	"vault_name":"Bath"
}, {
	"espn_name":"Clermont Auvergne",
	"vault_name":"Clermont"
}, {
	"espn_name":"Bristol Rugby",
	"vault_name":"Bristol"
},{
	"espn_name":"Stade Francais Paris",
	"vault_name":"Stade Francais"
},{
	"espn_name":"Castres Olympique",
	"vault_name":"Castres"
},{
	"espn_name":"Montpellier Herault",
	"vault_name":"Montpellier"
},{
	"espn_name":"Stade Toulousain",
	"vault_name":"Toulousain"
},]

def check_for_alternate_name(team_name):
	
	for team in alternate_names:
		if team["espn_name"] == team_name:
			team_name = team["vault_name"]
			
			return team_name

	return team_name


def make_soup(html):

	soupdata = BeautifulSoup(html, "html.parser")
	return soupdata

season_ids = [333, 100, 98, 96, 94]

years = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014]

for i, year in enumerate(years):

	print(i)

	try:
		url = 'https://au.eurosport.com/rugby/top-14/' + str(years[i + 1]) + '-' + str(years[i]) + '/calendar-result.shtml'
		res = requests.get(url)
		print(url)
		page_soup = make_soup(res.content)

		rounds = []

		round_divs = page_soup.findAll('div', {'class': 'rounds-dropdown__round'})

		for round_div in round_divs:
			rounds.append(round_div['data-round-id'])

		print(rounds)
		

		


		# date = datetime.today() - timedelta(days=i)
		# print(date)
		# url_date = date.strftime('%Y%m%d')

		# res = requests.get('https://au.eurosport.com/_ajax_/results_v8_5/results_teamsports_v8_5.zone?O2=1&site=eau&langueid=0&domainid=137&mime=text%2fxml&dropletid=3&sportid=44&revid=755&seasonid=333&SharedPageTheme=black&DeviceType=desktop&AnalyticsSportEvent=rugby-top14&roundid=5171')
		# soup = make_soup(res.content)

		# print('')

		

		# a_teams = soup.findAll('td', {'class': 'team-a'})
		# b_teams = soup.findAll('td', {'class': 'team-b'})


		# for a,b in zip(a_teams,b_teams):
		# 	team_one = a.find('abbr').get('title')
		# 	team_two = b.find('abbr').get('title')

		# 	team_one = check_for_alternate_name(team_one)
		# 	team_two = check_for_alternate_name(team_two)

		

		# 	try:

		# 		team_one_obj = Team.objects.filter(team_name=team_one)[0]
		# 		team_two_obj = Team.objects.filter(team_name=team_two)[0]



		# 	except:
		# 		print("FAILED: ",team_one,team_two)
		# 		continue




		# 	existing = Match.objects.filter(home_team=team_one_obj,away_team=team_two_obj).order_by('-date')

		# 	if len(existing) > 0:
		# 		if abs(existing[0].date - date) < timedelta(days=4):
		# 			#print("EXISTS: ",team_one,team_two)
		# 			continue

		# 	print("NEW: ",team_one,team_two)

		# 	new_match = Match(home_team=team_one_obj,away_team=team_two_obj,date=date,home_score=0,away_score=0,league_id=team_one_obj.league_id)
		# 	new_match.save()
	except Exception as e: 
		print(e)



