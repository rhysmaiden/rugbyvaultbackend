import django
import wikipedia
import os
import subprocess
import youtube_videos
import time
import datetime


import json
# from youtube_search_v2 import search

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Player
from rugby.models import Try
from rugby.models import League
import youtube_dl, subprocess

PLAYER_NAME = "Cheslin Kolbe"


league_object = League.objects.filter(name="International")[0]
player_object = Player.objects.filter(name=PLAYER_NAME)[0]

print(player_object.number_of_tries())
player_tries = Try.objects.filter(player=player_object).filter(match__date__year=2019,match__league_id=league_object).order_by('match__date')

print(len(player_tries))

if not os.path.exists("/Users/rhysmaiden/Documents/" + player_object.name):
    os.mkdir("/Users/rhysmaiden/Documents/" + player_object.name)



for index,try_object in enumerate(player_tries):


    URL = try_object.match.video_link
    FROM = str(datetime.timedelta(seconds=try_object.start_time - 5))
    TO = str(datetime.timedelta(seconds=try_object.end_time))
    TARGET = "/Users/rhysmaiden/Documents/" + try_object.player.name + "/" + try_object.player.name.replace(" ","") + str(index) + ".mp4"
    print(TARGET)
    with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
        result = ydl.extract_info(URL, download=False)
        video = result['entries'][0] if 'entries' in result else result

    url = video['url']

    subprocess.call('ffmpeg -i "%s" -ss %s -to %s -c:v copy -c:a copy "%s"' % (url, FROM, TO, TARGET),shell=True)

# command = "ffmpeg "

# for filename in os.listdir("Cheslin Kolbe"):
#     command += '-i "Cheslin Kolbe/' + filename + '" '
#     print(command)

# command += '\ -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" \
#   -map "[v]" -map "[a]" output.mkv



# with open(player_object.name + "/tries.txt",'w') as textFile:
#     for filename in os.listdir(player_object.name):
#         # print("/Users/rhysmaiden/Documents/Cheslin Kolbe/" + filename + "\n")
#         if "mp4" in filename:
#             textFile.write("file '" + filename + "'\n")



# command = 'ffmpeg -f concat -safe 0 -i "' + player_object.name + '/tries.txt" -c copy "' + player_object.name + '/output.mp4"'
# print(command)

# subprocess.call(command,shell=True)