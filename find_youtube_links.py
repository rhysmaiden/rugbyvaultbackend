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
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match

enddate = datetime.today()
startdate = enddate - timedelta(days=10000)

matches = Match.objects.filter(
    video_link_found=0).order_by('-date')


DEVELOPER_KEYS = ["AIzaSyBSqLs1LgVGrHhZ2hAQLemjruCFmNic1kA","AIzaSyAB3stHsYPoEogXmGGSfxCBzD9zlsh8D3E","AIzaSyDgSdNuzbho-hF1hjADW_OFpWlMp6J4img"]
code_index = 0

print(len(matches))

for match in matches:

    if match.video_link != "":
        continue

    start_time_period = match.date - timedelta(days=1)
    end_time_period = match.date + timedelta(days=16)

    found_videos = []

    try:
        found_videos = youtube_search(
        match.home_team.team_name + " vs " + match.away_team.team_name + " rugby highlights " + str(match.date.year), DEVELOPER_KEY=DEVELOPER_KEYS[code_index])
    except Exception as e:
        code_index += 1
        if code_index == 3:
            print("codes failed")   
            break
    
    foundVideo = False
    video_id = ""

    for video in found_videos:

        video_date = datetime.strptime(video.date[:10], "%Y-%m-%d")
        if video_date > start_time_period and video_date < end_time_period:
            if match.home_team.team_name in video.title and match.away_team.team_name in video.title:
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
