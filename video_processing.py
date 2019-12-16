from pytube import YouTube
import os
import subprocess
import time
import datetime
from datetime import datetime, timedelta

import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rugby.settings")
import django
django.setup()

from rugby.models import Match
from rugby.models import Try

time_period = datetime.today() - timedelta(days=7)
matches = Match.objects.filter(date__gte=time_period).filter(video_link_found=1).filter(video_downloaded=1)

for match in matches:
    tries = Try.objects.filter(match=match).order_by('minute')

    print(len(tries))
    for t in tries:
        print(t.player.name)

    if os.path.exists('videos/' + str(match.id) + '.mp4'):

        video_manager = VideoManager(['videos/' + str(match.id) + '.mp4'])
        stats_manager = StatsManager()
        scene_manager = SceneManager(stats_manager)

        scene_manager.add_detector(ContentDetector())
        base_timecode = video_manager.get_base_timecode()

        try:

            # Set downscale factor to improve processing speed (no args means default).
            video_manager.set_downscale_factor()

            # Start video_manager.
            video_manager.start()

            # Perform scene detection on video_manager.
            scene_manager.detect_scenes(frame_source=video_manager)

            # Obtain list of detected scenes.
            scene_list = scene_manager.get_scene_list(base_timecode)
            # Like FrameTimecodes, each scene in the scene_list can be sorted if the
            # list of scenes becomes unsorted.

            print('List of scenes obtained:')
            for i, scene in enumerate(scene_list):
                print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
                    i+1,
                    scene[0].get_timecode(), scene[0].get_frames(),
                    scene[1].get_timecode(), scene[1].get_frames(),))
        except:
            print("Erro")



        #os.system("scenedetect -i videos/" + str(match.id)  + '.mp4 -s list-scenes detect-content -t 70 split-video')
