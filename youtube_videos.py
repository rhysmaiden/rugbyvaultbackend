
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
#import pandas as pd
import pprint
#import matplotlib.pyplot as pd

DEVELOPER_KEY = "AIzaSyDt3Y3ZMJ3aiq24lDyo1cga2rgtF6PVhYU"
# DEVELOPER_KEY = "AIzaSyAB3stHsYPoEogXmGGSfxCBzD9zlsh8D3E"
DEVELOPER_KEY = "AIzaSyDgSdNuzbho-hF1hjADW_OFpWlMp6J4img"

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class Video:
    video_id = ""
    date = None



def youtube_search(q, max_results=3,order="relevance", token=None, location=None, location_radius=None):

    print("Starting search...")



    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", # Part signifies the different types of data you want
    maxResults=max_results,
    location=location,
    locationRadius=location_radius).execute()

    print("Got response")

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            #print(dir(search_result['id']))

            video = Video()
            video.video_id = search_result['id']['videoId']
            video.date = search_result['snippet']['publishedAt']
            videos.append(video)

    return videos

#print(youtube_search("Rugby"))
