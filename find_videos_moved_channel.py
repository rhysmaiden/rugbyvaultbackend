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
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match
from rugby.models import League
from rugby.models import Try

enddate = datetime.today()
startdate = enddate - timedelta(days=10000)

matches = Match.objects.filter(league_id = League.objects.filter(name="Super Rugby")[0]).order_by('-date')


DEVELOPER_KEYS = ["AIzaSyDAJZYGRINk-3XBpGdbliu3IFBjdPrWgj8","AIzaSyBSqLs1LgVGrHhZ2hAQLemjruCFmNic1kA","AIzaSyAB3stHsYPoEogXmGGSfxCBzD9zlsh8D3E","AIzaSyDgSdNuzbho-hF1hjADW_OFpWlMp6J4img","AIzaSyABtr4jUFpRcm4isj2EWjYfu1MjqzISF78"]
code_index = 0

print(len(matches))

for match in matches:

    current_vid_id = match.video_link.split('=')[-1]

    res = requests.get("https://www.googleapis.com/youtube/v3/videos?id=" + current_vid_id + "&part=contentDetails&key=" + DEVELOPER_KEYS[code_index])
    
    current_vid = res.json()

    try:   
        current_duration = current_vid['items'][0]['contentDetails']['duration']
    except Exception as e:
        if e == 'items':
            code_index += 1
        #match.error = 1
       # match.save()
        continue

    try:
        match.region_blocked = current_vid['items'][0]['contentDetails']['regionRestriction']['blocked'][0]
        if match.region_blocked == "AU":
            pass
            #print(match, match.region_blocked)
        else:
            continue
    except:
        continue

    #print(match, match.region_blocked)


    start_time_period = match.date - timedelta(days=1)
    end_time_period = match.date + timedelta(days=16)

    found_videos = []

    try:
        found_videos = youtube_search(
        match.home_team.team_name + " vs " + match.away_team.team_name + " rugby highlights " + str(match.date.year), DEVELOPER_KEY=DEVELOPER_KEYS[code_index])

     
    except Exception as e:
        print(e)
        code_index += 1
        if code_index == 3:
            print("codes failed")   
            break
    
    foundVideo = False
    video_id = ""

    for video in found_videos:
        res = requests.get("https://www.googleapis.com/youtube/v3/videos?id=" + video.video_id + "&part=contentDetails&key=" + DEVELOPER_KEYS[code_index])
    
        vid = res.json()

        vid_duration = None

        try:   
            vid_duration = vid['items'][0]['contentDetails']['duration']
        except:
            continue

        

        if vid_duration == current_duration:
            print("Old", match, match.video_link)
            match.video_link = "https://www.youtube.com/watch?v=" + video.video_id
            print("New", match, match.video_link)
            print(len(Try.objects.filter(match=match)), "Tries to convert")

        

        video_date = datetime.strptime(video.date[:10], "%Y-%m-%d")
        if video_date > start_time_period and video_date < end_time_period:
            if match.home_team.team_name in video.title or match.home_team.nickname:
                if match.away_team.team_name in video.title or match.away_team.nickname:
                    video_id = video.video_id
                    foundVideo = True
                    break

    # time.sleep()
