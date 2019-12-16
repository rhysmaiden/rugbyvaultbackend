import praw
import config
import time
import datetime
import time
import csv
import datetime
import os
import sys
from itertools import chain
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Match
from rugby.models import Player
from rugby.models import Try
from rugby.models import Team


def bot_login():
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="Test 1")
    return r

def recent_tries(comment):

    body = comment.body[13:]
    player = Player.objects.filter(name = body)[0]
    tries = Try.objects.filter(player = player).order_by('-match__date')[:5]

    table = "**" + body + "**\n"
    table += "|Match|Video Link|\n:--|:--|"

    for t in tries:
        table += "\n|" + str(t.match) + "|" + t.video_link

    return table

def recent_matches_twoteams(comment):

    body = comment.body[15:]

    teams = body.split(" vs ")

    team_1 = Team.objects.filter(team_name=teams[0])[0]
    team_2 = Team.objects.filter(team_name=teams[1])[0]

    matches_1 = Match.objects.filter(home_team=team_1,away_team=team_2)
    matches_2 = Match.objects.filter(home_team=team_2,away_team=team_1)

    matches = (matches_1 | matches_2).order_by('-date')[:5]



    table = "**" + body + "**\n"
    table += "|Date|Video Link|\n:--|:--|"

    for m in matches:
        table += "\n|" + str(m.date.date()) + "|" + m.video_link

    return table

def recent_matches_singleteam(comment):

    body = comment.body[15:]

    team = Team.objects.filter(team_name=body)[0]

    matches_1 = Match.objects.filter(home_team=team)
    matches_2 = Match.objects.filter(away_team=team)

    matches = (matches_1 | matches_2).order_by('-date')[:5]

    table = "**" + body + "**\n"
    table += "|Date|Video Link|\n:--|:--|"

    for m in matches:
        table += "\n|" + str(m.date.date()) + "|" + m.video_link

    return table

r = bot_login()

comment_ids = []

while True:

    try:
        for comment in r.subreddit('rugbyunion').stream.comments():

            if comment.id in comment_ids:
                continue

            comment_ids.append(comment.id)

            if "!recenttries" in comment.body:
                comment.reply(recent_tries(comment))
            elif "!recentmatches" in comment.body and "vs" in comment.body:
                comment.reply(recent_matches_twoteams(comment))
            elif "!recentmatches" in comment.body:
                comment.reply(recent_matches_singleteam(comment))
            else:
                pass


    except:
        time.sleep(1)
