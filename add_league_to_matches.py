import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Match
from rugby.models import League

matches = Match.objects.all()

ints = ["New Zealand","Wales","England","Ireland","South Africa","Australia",
"France","Japan","Scotland","Argentina","Fiji","Italy","Georgia","Samoa",
"USA","Tonga","Spain","Uruguay","Romania","Canada","Namibia","Russia"]

prem = ["Worcester Warriors","Northampton Saints","Leicester Tigers","Saracens",
"Sale Sharks","Gloucester","Bath","London Irish","Newcastle Falcons","Harlequins","Wasps",
"Exeter Chiefs"]

pro_14 = ["Zebre","Benetton Treviso","Edinburgh","Glasgow Warriors","Cardiff Blues",
"Dragons","Ospreys","Scarlets","Connacht","Ulster","Munster","Leinster"]

super_teams = ["Brumbies","New South Wales Waratahs","Queensland Reds","Force",
"Melbourne Rebels","Crusaders","Highlanders","Hurricanes","Chiefs",
"Blues","Sharks","Bulls","Stormers","Lions","Jaguares","Sunwolves"]



for match in matches:
	if match.home_team.team_name in ints:
		match.league_id = League.objects.filter(name="International")[0]
	elif match.home_team.team_name in prem:
		match.league_id = League.objects.filter(name="Aviva Premiership")[0]
	elif match.home_team.team_name in pro_14:
		match.league_id = League.objects.filter(name="Pro 14")[0]
	elif match.home_team.team_name in super_teams:
		match.league_id = League.objects.filter(name="Super Rugby")[0]
	else:
	    match.league_id = League.objects.filter(name="Top 14")[0]


	match.save()
	print(match,match.league_id)