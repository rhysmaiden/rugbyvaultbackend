from datetime import datetime
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import namedtuple
from .serializers import HighlightSerializer
from .serializers import PlayerSerializer
from .serializers import MatchSerializer
from .serializers import TrySerializer
from .serializers import TeamSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import SubmitUrlForm
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView, DetailView
from.models import Player
from.models import Team
from.models import Match
from.models import Try
from.models import League
from.models import MatchRating
from.models import TryRating

import re

import urllib
import urllib.request
from bs4 import BeautifulSoup
# from .filters import TryFilter

alternate_names = [{
	"espn_name":"Gloucester Rugby",
	"vault_name":"Gloucester"
}, {
	"espn_name":"Bath Rugby",
	"vault_name":"Bath"
}, {
	"espn_name":"Clermont Auvergne",
	"vault_name":"Clermont"
}, {
	"espn_name":"Bristol Rugby",
	"vault_name":"Bristol"
},{
	"espn_name":"Stade Francais Paris",
	"vault_name":"Stade Francais"
},{
	"espn_name":"Castres Olympique",
	"vault_name":"Castres"
},{
	"espn_name":"Montpellier Herault",
	"vault_name":"Montpellier"
},{
	"espn_name":"Stade Toulousain",
	"vault_name":"Toulousain"
},]

def check_for_alternate_name(team_name):
	
	for team in alternate_names:
		if team["espn_name"] == team_name:
			team_name = team["vault_name"]
			
			return team_name

	return team_name

def make_soup(url):
    try:
        print(url)
        thepage = urllib.request.urlopen(url)
        soupdata = BeautifulSoup(thepage, "html.parser")

        return soupdata
    except urllib.error as e:
        print(e)
	
    return True


@csrf_exempt
def tryprocessing(request):

    my_context = {
        "match": [],
        "tries": [],
        "video_link": [],
        "players": [],
        "amount": [],
        "page": "",
        "try_count": ""
    }

    my_context["amount"] = len(Match.objects.filter(
        video_link_found=1, match_completely_processed=0, error=0))
    my_context["try_count"] = len(Try.objects.all())

    tries = Try.objects.all()

    aviva_league = League.objects.filter(name="Aviva Premiership")[0]
    pro_league = League.objects.filter(name="Pro 14")[0]
    super_league = League.objects.filter(name="Super Rugby")[0]
    international_league = League.objects.filter(name="International")[0]

    # Get the latest match
    latest_match = Match.objects.filter(
        video_link_found=1, match_completely_processed=0, error=0).order_by('-date')[0]
    my_context["match"] = latest_match

    if request.method == "POST":

        if "finished" in request.POST:
            latest_match.match_completely_processed = 1
            latest_match.save()
        elif "error" in request.POST:
            latest_match.error = 1
            latest_match.save()
        else:
            player_name = request.POST['player_name']
            start_time_minute = request.POST['start_time_minute']
            start_time_second = request.POST['start_time_second']
            end_time_minute = request.POST['end_time_minute']
            end_time_second = request.POST['end_time_second']
            team_id = int(request.POST['team_id'])

            start_time = minutes_and_seconds_to_seconds(
                int(start_time_minute), int(start_time_second))
            end_time = minutes_and_seconds_to_seconds(
                int(end_time_minute), int(end_time_second))
            new_link = add_times_to_video_link(
                latest_match.video_link, start_time, end_time)

            try_scorer_object = Player.objects.filter(name=player_name)[0]
            team_from_id = Team.objects.filter(id=team_id)[0]

            try_object = Try(match=latest_match, player=try_scorer_object, video_link=new_link,
                             start_time=start_time, end_time=end_time, team=team_from_id)

            if int(team_id) < 63 and int(team_id) > 44:
                try_scorer_object.internation_team = team_from_id
                try_scorer_object.save()

            try_object.save()

            return HttpResponse('success')

        return render(request, 'rugby/tryprocessing.html', {})

    else:

        my_context["players"] = Player.objects.all()

        if "embed" not in latest_match.video_link:
            print(latest_match.video_link)
            my_context["video_link"] = "https://www.youtube.com/embed/" + \
                latest_match.video_link.split("=")[1] + "?rel=0"
        else:
            my_context["video_link"] = latest_match.video_link + "?rel=0"

        return render(request, 'rugby/tryprocessing.html', my_context)


def minutes_and_seconds_to_seconds(minutes, seconds):

    seconds_from_minutes = minutes * 60
    return seconds + seconds_from_minutes


def add_times_to_video_link(video_link, start_time, end_time):
    try:
        link = "https://www.youtube.com/embed/" + \
            video_link.split("=")[1] + "?start=" + \
            str(start_time) + "&end=" + str(end_time) + ";rel=0"
    except:
        return video_link

    return link


def youtube_to_embed(original):
    print(original)

    if 'embed' in original:
        return original

    embedded = "https://www.youtube.com/embed/" + original.split("=")[1]
    return embedded


# REST FRAMEWORK
Highlight = namedtuple('Highlights', ('players', 'matches', 'tries', 'teams'))

class Highlights(APIView):
    def get(self, request):

        print(
            '{timestamp} -- request started'.format(timestamp=datetime.utcnow().isoformat()))

        league_name = ""
        league = None

        try:
            league_name = request.GET.get('league')

            if league_name == "international":
                league = League.objects.filter(name="International")[0]
            elif league_name == "superrugby":
                league = League.objects.filter(name="Super Rugby")[0]
            elif league_name == "aviva":
                league = League.objects.filter(name="Aviva Premiership")[0]
            
        except:
            pass

        # Recent request
        matches = Match.objects.filter(
            video_link_found=1, error=0).order_by('-date')

        if league_name != None:
            matches = matches.filter(league_id=league)[:12]
            
        else:
            matches = matches[:12]


        tries = Try.objects.filter(error=0).order_by('-match__date')[:12]

        print(
            '{timestamp} -- obtained data'.format(timestamp=datetime.utcnow().isoformat()))

        
        match_serializer = MatchSerializer(
            matches, many=True)
        try_serializer = TrySerializer(
            tries, many=True)

        print(
            '{timestamp} -- finished serializing'.format(timestamp=datetime.utcnow().isoformat()))

        return Response({
            "matches": match_serializer.data,
            "tries": try_serializer.data
        })


class PlayerAPI(APIView):
    def get(self, request):

        player_id = request.GET.get('id')
        order = request.GET.get('order')

        print(player_id)

        player = Player.objects.filter(id=player_id)[0]

        teams = Team.objects.filter(
            id__in=[player.team.id, player.internation_team.id])

        tries = Try.objects.filter(
            player=player_id, error=0)

        if order == "date":
            tries = tries.order_by('-match__date')
        elif order == "rating":
            tries = sorted(tries, key=lambda x: x.avg_rating(), reverse=True)
            # tries.order_by('-avg_rating')

        try_serializer = TrySerializer(tries, many=True)
        player_serializer = PlayerSerializer(player, many=False)
        team_serializer = TeamSerializer(teams, many=True)

        return Response({
            "player": player_serializer.data,
            "teams": team_serializer.data,
            "tries": try_serializer.data
        })


class TeamAPI(APIView):
    def get(self, request):

        team_id = request.GET.get('id')
        order = request.GET.get('order')

        team = Team.objects.filter(id=team_id)[0]

        players = Player.objects.filter(
            Q(team=team) | Q(internation_team=team))

        matches = Match.objects.filter(Q(home_team=team) | Q(
            away_team=team)).filter(error=0, video_link_found=1)

        tries = Try.objects.filter(
            team=team, error=0)

        if order == "date":
            matches = matches.order_by('-date')
            tries = tries.order_by('-match__date')[:12]
        elif order == "rating":
            matches = sorted(
                matches, key=lambda x: x.avg_rating(), reverse=True)
            tries = sorted(tries, key=lambda x: x.avg_rating(),
                           reverse=True)[:12]

        team_serializer = TeamSerializer(team, many=False)
        player_serializer = PlayerSerializer(players, many=True)
        match_serializer = MatchSerializer(matches, many=True)
        try_serializer = TrySerializer(tries, many=True)

        return Response({
            "team": team_serializer.data,
            "players": player_serializer.data,
            "matches": match_serializer.data,
            "tries": try_serializer.data
        })


class MatchHistoryAPI(APIView):

    def get(self, request):

        home_team_id = request.GET.get('home_team')
        away_team_id = request.GET.get('away_team')

        teams = Team.objects.filter(Q(id=home_team_id) | Q(
            id=away_team_id))

        matches = Match.objects.filter(Q(
            home_team__in=[teams[0].id, teams[1].id]) & Q(away_team__in=[teams[0].id, teams[1].id])).filter(error=0).order_by('-date')

        tries = Try.objects.filter(
            match__in=matches).filter(error=0).order_by('-match__date')[:10]

        team_serializer = TeamSerializer(teams, many=True)
        match_serializer = MatchSerializer(matches, many=True)
        try_serializer = TrySerializer(tries, many=True)

        return Response({
            "teams": team_serializer.data,
            "matches": match_serializer.data,
            "tries:": try_serializer.data
        })


class VideoAPI(APIView):
    def get(self, request):

        if request.GET.get('type') == "try":
            single_try = Try.objects.filter(id=request.GET.get('id'))[0]
            player_tries = Try.objects.filter(
                player=single_try.player, error=0)[:12]

            single_try_serializer = TrySerializer(single_try, many=False)
            player_tries_serializer = TrySerializer(player_tries, many=True)

            return Response({
                "try": single_try_serializer.data,
                "player_tries": player_tries_serializer.data
            })

        elif request.GET.get('type') == "match":

            match = Match.objects.filter(id=request.GET.get('id'))[0]

            rating_object = MatchRating.objects.filter(
                match=match, userId=request.GET.get('googleId'))
            rating = 0
            if len(rating_object) > 0:
                rating = rating_object[0].rating

            matches = Match.objects.filter(Q(
                home_team__in=[match.home_team, match.away_team]) & Q(away_team__in=[match.home_team, match.away_team])).filter(error=0).order_by('-date')[:10]

            match_serializer = MatchSerializer(match, many=False)
            matches_serializer = MatchSerializer(matches, many=True)

            return Response({
                "match": match_serializer.data,
                "matches": matches_serializer.data,
                "rating": rating

            })


class RatingAPI(APIView):
    def post(self, request):

        body = json.loads(request.body.decode('utf-8'))
        print(body)
        if request.GET.get('type') == "match":
            match = MatchRating.objects.filter(
                userId=body['googleId'], match=body['id'])
            if len(match) == 0:
                newrating = MatchRating(
                    userId=body['googleId'], match=Match.objects.filter(id=body['id'])[0], rating=body['rating'])
                newrating.save()
            else:
                match[0].rating = body['rating']
                match[0].save()
        elif request.GET.get('type') == "try":
            try_obj = TryRating.objects.filter(
                userId=body['googleId'], try_obj=body['id'])
            if len(try_obj) == 0:
                newrating = TryRating(
                    userId=body['googleId'], try_obj=Try.objects.filter(id=body['id'])[0], rating=body['rating'])
                newrating.save()
            else:
                try_obj[0].rating = body['rating']
                try_obj[0].save()

        return Response(None)


class ChartAPI(APIView):
    def get(self, request):
        object_list = []
        type = request.GET.get('type')
        requested_range = request.GET.get('range')

        if type == "match":
            object_list = Match.objects.all()

            if requested_range == "allTime":
                object_list = object_list

            elif requested_range == "thisMonth":
                object_list = object_list.filter(
                    date__month=datetime.now().month, date__year=datetime.now().year)

            elif requested_range == "thisYear":
                object_list = object_list.filter(
                    date__year=datetime.now().year)

            print("start")
            object_list = sorted(
                object_list, key=lambda x: x.avg_rating(), reverse=True)[:20]

            print("end")

            matches_serializer = MatchSerializer(object_list, many=True)

            return Response({
                "matches": matches_serializer.data
            })

        elif type == "try":
            object_list = Try.objects.all()

            if requested_range == "allTime":
                object_list = object_list

            elif requested_range == "thisMonth":
                object_list = object_list.filter(
                    match__date__month=datetime.now().month, match__date__year=datetime.now().year)

            elif requested_range == "thisYear":
                object_list = object_list.filter(
                    match__date__year=datetime.now().year)

            object_list = sorted(
                object_list, key=lambda x: x.avg_rating(), reverse=True)[:20]

            tries_serializer = TrySerializer(object_list, many=True)

            return Response({
                "tries": tries_serializer.data
            })


class SearchAPI(APIView):
    def get(self, request):
        query = request.GET.get('query')

        teams = Team.objects.filter(team_name__contains=query)[:3]
        players = Player.objects.filter(name__contains=query)[:3]

        searchResults = []

        for t in teams:
            search_object = {"id": t.id, "name": t.team_name, "type": "team"}
            searchResults.append(search_object)

        for p in players:
            search_object = {"id": p.id, "name": p.name, "type": "player"}
            searchResults.append(search_object)

        return Response(searchResults)

class TryProcessingAPI(APIView):
    
    def get(self, request):
       
        match_id = request.GET.get('id')

        league = League.objects.filter(name__in=["Mitre 10","USA","Top 14"])
        league_1 = league[0]
        league_2 = league[1]
        league_3 = league[2]
        league_super = League.objects.filter(name="Super Rugby")[0]

        if match_id == 'undefined':
            match_object = Match.objects.filter(match_completely_processed=0,video_link_found=1,error=0,league_id=league_super).exclude(league_id__in=[league_1,league_2,league_3]).order_by('-date')[0]
            print(match_object)
        else:
            match_object = Match.objects.filter(id=match_id)[0]

        match_serializer = MatchSerializer(match_object,many=False)

        scoreboard_url = "https://www.espn.co.uk/rugby/scoreboard?date=" + str(match_object.date.year) + str("{:02d}".format(match_object.date.month)) + str("{:02d}".format(match_object.date.day))
        soup = make_soup(scoreboard_url)

        print(match_object)
        
        games = soup.findAll('div', {'class': 'scoreboard-wrapper'})
        teams = soup.findAll('span', {'class': 'short-name'})

        game_index = 0

        # There are double the number of teams to games
        for index,team in enumerate(teams):
            team_text = check_for_alternate_name(team.text)
			
            if match_object.home_team.team_name == team_text:
                if index % 2 == 1:
                    index -= 1
                
                game_index = int(index/2)
                break
        
        game = games[game_index]

        home_block = game.find('div',{'class','home'})
        away_block = game.find('div',{'class','away'})

        home_players = []
        away_players = []

        try:
            home_players = home_block.find('ul',{'class','icon-rugby-solid'}).findAll('li')
        except:
            print("No home tries")
        
        try:
            away_players = away_block.find('ul',{'class','icon-rugby-solid'}).findAll('li')
        except:
            print("No away tries")

        players = home_players + away_players

        player_dicts = []

        for counter, player in enumerate(players):

            player_name = player.find('a').text

            try:
                player_object = Player.objects.filter(name=player_name)[0]
            except:
                if counter > len(home_players) - 1:
                    player_object = Player(name=player_name, team=match_object.away_team)
                    player_object.save()
                else:
                    player_object = Player(name=player_name, team=match_object.home_team)
                    player_object.save()

            time_unclean = player.find('span').text
            times = time_unclean.split(',')

            for t in times:
                time_cleaned = int(re.search(r'\d+', t).group())
                player_dict = {'player_name':player_name, 'time':time_cleaned, 'id':player_object.id}
                player_dicts.append(player_dict)
                   
        players_sorted = sorted(player_dicts, key=lambda k: k['time'])    
        
        return Response({"players":players_sorted,"match":match_serializer.data})

class AddTryAPI(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))

        print(body['tries'])

        match = Match.objects.filter(id=body['match']['id'])[0]

        # Recieve: player_id, match_id, time (need to convert to seconds - done in frontend), 
        for trie in body['tries']:
            start_time = trie['start_time']
            end_time = trie['end_time']

            
            player = Player.objects.filter(id=trie['id'])[0]

            
            video_link = "https://www.youtube.com/embed/" + match.video_link.split('=')[1] + "?start=" + str(start_time) + "&end=" + str(end_time) + ";rel=0"

            try_object = Try(match=match,player=player,start_time=start_time,
            end_time=end_time,video_link=video_link)

            print(try_object)

            try_object.save()

        match.match_completely_processed = 1
        print(match)
        match.save()

        return Response(None)


class ReportAPI(APIView):
    def post(self, request):

        print("REPORT")

        body = json.loads(request.body.decode('utf-8'))
        
        if body['type'] == "match":
            match = Match.objects.filter(id=body['id'])[0]
            match.error = 1
            match.save()
        else:
            try_obj = Try.objects.filter(id=body['id'])[0]
            try_obj.error = 1
            try_obj.save()

        return Response(None)



