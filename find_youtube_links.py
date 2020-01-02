# Run script every 3 hours



import django
import wikipedia
import os
import subprocess
import youtube_videos
import time
import datetime
from youtube_videos import youtube_search
from datetime import datetime, timedelta
from youtube_search import YoutubeSearch
import json
# from youtube_search_v2 import search

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match
from rugby.models import League

league = League.objects.filter(name="Pro 14")[0]



enddate = datetime.today()
startdate = enddate - timedelta(days=1000)

print(startdate, enddate)
matches = Match.objects.filter(
    video_link_found=0,league_id=league).order_by('-date')


DEVELOPER_KEYS = ["AIzaSyDt3Y3ZMJ3aiq24lDyo1cga2rgtF6PVhYU","AIzaSyAB3stHsYPoEogXmGGSfxCBzD9zlsh8D3E","AIzaSyDgSdNuzbho-hF1hjADW_OFpWlMp6J4img"]
code_index = 0

for match in matches:

    if match.video_link != "":
        continue

    start_time_period = match.date - timedelta(days=1)
    end_time_period = match.date + timedelta(days=16)

    found_videos = []

    # results = YoutubeSearch(match.home_team.team_name + " v " + match.away_team.team_name + " rugby highlights " + str(match.date.year), max_results=10).to_json()

    # json_videos = json.loads(results)["videos"]

    

    # for vid in json_videos:
    #     print(vid)

    try:
        # print(DEVELOPER_KEYS[code_index])
        found_videos = youtube_search(
        match.home_team.team_name + " v " + match.away_team.team_name + " rugby highlights " + str(match.date.year),DEVELOPER_KEY=DEVELOPER_KEYS[code_index])
    except Exception as e:
        print(e)
        code_index += 1
        print("Up")
        if code_index == 3:   
            break
    
    foundVideo = False
    video_id = ""

    for video in found_videos:

        video_date = datetime.strptime(video.date[:10], "%Y-%m-%d")
        # print(match.date.day, video_date.day, start_time_period.day,end_time_period.day)
        if video_date > start_time_period and video_date < end_time_period:
            video_id = video.video_id
            foundVideo = True
            break
        else:
            pass

    if foundVideo:
        match.video_link_found = 1
        match.video_link = "https://www.youtube.com/watch?v=" + video_id

        print("Found: " + str(match))
        match.save()
    else:
        match.video_not_found = 1
        match.save()
        print("Didn't Find: " + str(match))

    # time.sleep()
