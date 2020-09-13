
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import os
import subprocess
import django
import re
import difflib
import praw

def prior_week_end():
    return datetime.now() - timedelta(days=((datetime.now().isoweekday()) % 7))

def prior_week_start():
    return prior_week_end() - timedelta(days=6)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()

from rugby.models import Match
from rugby.models import Team
from rugby.models import Player
from rugby.models import Try
from rugby.models import League

super_league = League.objects.filter(name="Super Rugby")[0]
matches = Match.objects.filter(date__range=(prior_week_start(), prior_week_end()), error=0, match_completely_processed=1)

tries = Try.objects.filter(match__in=matches)

output = "Here are the weeks match highlights and tries. You can find the rest of our collection at [The Rugby Vault](http://therugbyvault.com)"
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

post_body = output

reddit = praw.Reddit(client_id="h06MkxMmjq9wXQ", client_secret="2_UdJIXdTHV4zgitHZT9a6PQpEg", user_agent="my user agent", username=os.environ.get('REDDIT_USERNAME'), password=os.environ.get('REDDIT_PASSWORD'))

post_title = 'Match and Try Highlights (' + prior_week_start().strftime("%d %b, %Y") + ' - ' + prior_week_end().strftime("%d %b, %Y") + ')'
subreddit = 'test'

reddit.subreddit("test").submit(post_title, selftext=post_body)

print(output)





