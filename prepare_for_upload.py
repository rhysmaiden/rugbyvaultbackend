import os
import django
import youtube_dl, subprocess
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
django.setup()
from rugby.models import Match
from rugby.models import Try
from rugby.models import Player
from datetime import datetime, timedelta

def download_video(try_object, type):
    URL = try_object.match.video_link
    FROM = str(timedelta(seconds=try_object.start_time))
    TO = str(timedelta(seconds=try_object.end_time))
    TARGET = os.getcwd() + "/instagram/" + try_object.player.name.replace(" ","") + ".mp4"

    with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
        result = ydl.extract_info(URL, download=False)
        video = result['entries'][0] if 'entries' in result else result

    url = video['url']

    subprocess.call('ffmpeg -i "%s" -qscale 0 -ss "%s" -to "%s" "%s"' % (url, FROM, TO, TARGET),shell=True)

    UPPER_TEXT = ""
    OUTPUT = ""
    
    if type == "best_try_today":
        UPPER_TEXT = "ON THIS DAY - " + try_object.match.date.strftime('%d/%m/%Y')
        OUTPUT = "best_try_today.mp4"
        LOWER_TEXT = try_object.player.name + " (" + str(try_object.match.home_team.team_name) + " vs " + str(try_object.match.away_team.team_name) + ")"
    elif "random_try" in type:
        UPPER_TEXT = try_object.match.date.strftime('%d/%m/%Y')
        OUTPUT = type + ".mp4"
        LOWER_TEXT = try_object.player.name + " (" + str(try_object.match.home_team.team_name) + " vs " + str(try_object.match.away_team.team_name) + ")"
    
    subprocess.call('ffmpeg -y -i "%s" -filter_complex \
                    "[0:v]pad=iw:ih+200:0:(oh-ih)/2:color=white, \
                    drawtext=text=''%s'':fontfile=/Library/Fonts/Atial Unicode.ttf:fontsize=40:x=(w-tw)/2:y=(100-th)/2, \
                    drawtext=text=''%s'':fontfile=/Library/Fonts/Atial Unicode.ttf:fontsize=40:x=(w-tw)/2:y=h-50-(th/2)" \
                    instagram/%s' % (TARGET, UPPER_TEXT, LOWER_TEXT, OUTPUT),shell=True)

    subprocess.call('rm %s' % (TARGET) ,shell=True)


month = int(datetime.now().strftime('%m'))
day = int(datetime.now().strftime('%d'))

print(len(Try.objects.filter(match__date__year=2020)))

try:    
    # best_try_today = Try.objects.filter(match__date__month=month, match__date__day=day).order_by('-elo_rating')[0]
    # download_video(best_try_today, "best_try_today")

    random_tries = Try.objects.filter(error=0,elo_rating__gte=1015)
    print(len(random_tries))

    random_try_index_1 = random.randint(0, len(random_tries))
    random_try_index_2 = random.randint(0, len(random_tries))
    random_try_1 = random_tries[random_try_index_1]
    random_try_2 = random_tries[random_try_index_2]

    download_video(random_try_1, "random_try_1")
    download_video(random_try_2, "random_try_2")
    download_player_countdown("Jordie Barrett", 5)



    
except:
    print("No try today")

