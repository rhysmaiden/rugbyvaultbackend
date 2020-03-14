
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
from rugby.models import League

super_league = League.objects.filter(name="Super Rugby")[0]
matches = Match.objects.filter(date__gte=datetime.now()-timedelta(days=5))

tries = Try.objects.filter(match__in=matches)

output = "Here are the weeks match highlights and tries. You can find the rest of our collection at [The Rugby Vault](http://therugbyvault.com)"
output += "\n\n&nbsp;\n\n"
output += "***How to rate:*** To leave a rating on a match or try you can do so by clicking the stars underneath the video. Hopefully by the end of the season we can have a good ranking of tries and matches as determined by fans."
output += "\n\n&nbsp;\n\n"
output += "#Match Highlights\n"
output += "| Match  | Video Link  |\n|:-----------|------------:|\n"

for match in matches:
	output += "| "
	match_string = str(match.home_team.team_name) + " vs " + str(match.away_team.team_name)
	output += match_string
	output += " | "
	link_string = "https://www.therugbyvault.com/video/match/" + str(match.id)
	output += link_string
	output += "|\n"

output += "\n\n&nbsp;\n\n"

output += "#Try Highlights\n"
output += "| Player Name | Match  | Video Link  |\n|:-----------|------------|------------:|\n"

for trie in tries:
	output += "| "
	player_string = trie.player.name
	output += player_string
	output += " | "

	match_string = str(trie.match.home_team.team_name) + " vs " + str(trie.match.away_team.team_name)
	output += match_string
	output += "|"



	link_string = "https://www.therugbyvault.com/video/try/" + str(trie.id)
	output += link_string
	output += "|\n"

print(output)





