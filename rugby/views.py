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
from rest_framework.decorators import action

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
from .models import Instagram

import math
from datetime import datetime
from datetime import timedelta

import re
import random

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

def youtube_to_embed(original):
	print(original)

	if 'embed' in original:
		return original

	embedded = "https://www.youtube.com/embed/" + original.split("=")[1]
	return embedded

def query_year_for_matches(matches,yearsParam):
	if yearsParam[0] != "all":
		yearsParam = [ int(x) for x in yearsParam ]
		matches = matches.filter(date__year__in=yearsParam)
	
	return matches

def query_year_for_tries(tries,yearsParam):
	if yearsParam[0] != "all":
		yearsParam = [ int(x) for x in yearsParam ]
		tries = tries.filter(match__date__year__in=yearsParam)
	
	return tries

def query_team_for_matches(matches,teamsParam):
	if teamsParam[0] != "all":
		teams = Team.objects.filter(team_name__in=teamsParam)
		matches = matches.filter(Q(home_team__in=teams) | Q(away_team__in=teams))

	return matches

def query_team_for_tries(tries,teamsParam):
	if teamsParam[0] != "all":
		teams = Team.objects.filter(team_name__in=teamsParam)
		tries = tries.filter(Q(match__home_team__in=teams) | Q(match__away_team__in=teams))

	return tries

def query_league_for_matches(matches,leagueParam):
	if leagueParam[0] != "all":
	   league = League.objects.filter(name__in=leagueParam)[0]
	   matches = matches.filter(league_id=league)

	return matches

def query_league_for_tries(tries,leagueParam):
	if leagueParam[0] != "all":
	   
	   league = League.objects.filter(name__in=leagueParam)[0]
	   tries = tries.filter(match__league_id=league)

	return tries

def filter_year_for_matches(matches,yearsParam):
	
	yearsFilter = []
	
	if yearsParam[0] == "all":
		dates = [d.year for d in matches.datetimes('date', 'year')]
		
		for year in reversed(dates):
			yearsFilter.append({"value":year,"checked":False})
	else:
		for year in yearsParam:
			yearsFilter.append({"value":year,"checked":True})

	return yearsFilter

def filter_year_for_tries(tries,yearsParam):

	yearsFilter = []
	
	if yearsParam[0] == "all":
		dates = [d.year for d in tries.datetimes('match__date', 'year')]
		
		for year in reversed(dates):
			yearsFilter.append({"value":year,"checked":False})
	else:
		for year in yearsParam:
			yearsFilter.append({"value":year,"checked":True})

	return yearsFilter

def filter_team_for_matches(matches,teamsParam):
	teamsFilter = []

	if teamsParam[0] == "all":
		teams = set(matches.values_list('home_team__team_name',flat=True).distinct())
		teams = teams | set(matches.values_list('away_team__team_name',flat=True).distinct())

		for t in teams:
			teamsFilter.append({"value":t,"checked":False})
	else:
		teams = set(matches.values_list('home_team__team_name',flat=True).distinct())
		teams = teams | set(matches.values_list('away_team__team_name',flat=True).distinct())

		for t in teams:
			
			if t not in teamsParam:
				teamsFilter.append({"value":t,"checked":False})
			else:
				teamsFilter.append({"value":t,"checked":True})

	return teamsFilter       


def filter_team_for_tries(tries,teamsParam):
	teamsFilter = []

	teams = set(tries.values_list('match__home_team__team_name',flat=True).distinct())
	teams = teams | set(tries.values_list('match__away_team__team_name',flat=True).distinct())

	if teamsParam[0] == "all":
		for t in teams:
			teamsFilter.append({"value":t,"checked":False})
	else:
		for t in teams:     
			if t not in teamsParam:
				teamsFilter.append({"value":t,"checked":False})
			else:
				teamsFilter.append({"value":t,"checked":True})

	return teamsFilter       

def filter_league_for_matches(matches,leaguesParam):
	leagueFilter = []

	leagues = set(matches.values_list('league_id__name',flat=True).distinct())

	if leaguesParam == "all":
		for l in leagues:
			leagueFilter.append({"value":l,"checked":False})
	else:
		for l in leagues:
			if l not in leaguesParam:
				leagueFilter.append({"value":l,"checked":False})
			else:
				leagueFilter.append({"value":l,"checked":True})

	return leagueFilter

def filter_league_for_tries(tries,leaguesParam):
	leagueFilter = []

	leagues = set(tries.values_list('match__league_id__name',flat=True).distinct())

	if leaguesParam == "all":
		for l in leagues:
			leagueFilter.append({"value":l,"checked":False})
	else:
		for l in leagues:
			if l not in leaguesParam:
				leagueFilter.append({"value":l,"checked":False})
			else:
				leagueFilter.append({"value":l,"checked":True})

	return leagueFilter


# REST FRAMEWORK
Highlight = namedtuple('Highlights', ('players', 'matches', 'tries', 'teams'))

class Highlights(APIView):
	def get(self, request):

		# print(
		# 	'{timestamp} -- request started'.format(timestamp=datetime.utcnow().isoformat()))

		league_name = ""
		league_try_name = ""
		league = None
		try_league = None

		try:
			league_name = request.GET.get('league_match')

			if league_name == "international":
				league = League.objects.filter(name="International")[0]
			elif league_name == "superrugby":
				league = League.objects.filter(name="Super Rugby")[0]
			elif league_name == "aviva":
				league = League.objects.filter(name="Aviva Premiership")[0]
			elif league_name == "pro14":
				league = League.objects.filter(name="Pro 14")[0]
			elif league_name == "usa":
				league = League.objects.filter(name="USA")[0]
			elif league_name == "mitre10":
				league = League.objects.filter(name="Mitre 10")[0]
			
		except:
			pass

		try:
			league_try_name = request.GET.get('league_try')

			if league_try_name == "international":
				try_league = League.objects.filter(name="International")[0]
			elif league_try_name == "superrugby":
				try_league = League.objects.filter(name="Super Rugby")[0]
			elif league_try_name == "aviva":
				try_league = League.objects.filter(name="Aviva Premiership")[0]
			elif league_try_name == "pro14":
				try_league = League.objects.filter(name="Pro 14")[0]
			elif league_try_name == "usa":
				try_league = League.objects.filter(name="USA")[0]
			elif league_try_name == "mitre10":
				try_league = League.objects.filter(name="Mitre 10")[0]
			
		except:
			pass

		# Recent request
		matches = Match.objects.filter(
			video_link_found=1, error=0).order_by('-date')

		print(matches)

		if league_name != "all":
			matches = matches.filter(league_id=league)
			
		
		matches = matches[:12]


		tries = Try.objects.filter(error=0).order_by('-match__date')

		if league_try_name != "all":
			tries = tries.filter(match__league_id=try_league)[:12]
			
		else:
			tries = tries[:12]

		# print(
		# 	'{timestamp} -- obtained data'.format(timestamp=datetime.utcnow().isoformat()))

		
		match_serializer = MatchSerializer(
			matches, many=True)
		try_serializer = TrySerializer(
			tries, many=True)

		# print(
		# 	'{timestamp} -- finished serializing'.format(timestamp=datetime.utcnow().isoformat()))

		return Response({
			"matches": match_serializer.data,
			"tries": try_serializer.data
		})


class PlayerAPI(APIView):
	def get(self, request):

		player_id = request.GET.get('id')
		order = request.GET.get('order')
		yearsParam = request.GET.get('year').split(",")
		teamsParam = request.GET.get('team').split(",")
		leaguesParam = request.GET.get('league').split(",")
		pageNumber = int(request.GET.get('page'))

		player = Player.objects.filter(id=player_id)[0]
		tries = Try.objects.filter(player=player)

		#Filter information for querying database
		tries = query_year_for_tries(tries,yearsParam)    
		tries = query_team_for_tries(tries,teamsParam)
		tries = query_league_for_tries(tries,leaguesParam)

		# Filter information for front end
		yearsFilter = filter_year_for_tries(tries,yearsParam)
		teamsFilter = filter_team_for_tries(tries,teamsParam)
		leaguesFilter = filter_league_for_tries(tries,leaguesParam)

		# Ordering
		if order == "date":
			tries = tries.order_by('-match__date')
		elif order == "rating":
			tries = tries.order_by('-ratings_average')

		pageCount = math.ceil(len(tries)/24)

		startIndex = (pageNumber - 1) * 24
		endIndex = startIndex + 24
		tries = tries[startIndex:endIndex]

		#Serializing
		try_serializer = TrySerializer(tries, many=True)
		player_serializer = PlayerSerializer(player, many=False)

		return Response({
			"player": player_serializer.data,
			"tries": try_serializer.data,
			"yearFilter": yearsFilter,
			"teamFilter": teamsFilter,
			"leagueFilter": leaguesFilter,
			"pageCount": pageCount
		})


class TeamAPI(APIView):
	def get(self, request):

		team_id = request.GET.get('id')
		order = request.GET.get('order')
		pageNumber = int(request.GET.get('page'))

		yearsParam = request.GET.get('year').split(",")
		teamsParam = request.GET.get('team').split(",")
		leaguesParam = request.GET.get('league').split(",")
		team = Team.objects.filter(id=team_id)[0]

		matches = Match.objects.filter(Q(
			home_team=team) | Q(away_team=team)).filter(error=0)

		print(len(matches))

		# Ordering
		if order == "date":
			matches = matches.order_by('-date')
		elif order == "rating":
			matches = matches.order_by('-ratings_average')

		#Filter information for querying database
		matches = query_year_for_matches(matches,yearsParam)    
		matches = query_team_for_matches(matches,teamsParam)
		matches = query_league_for_matches(matches,leaguesParam)

		# Filter information for front end
		yearsFilter = filter_year_for_matches(matches,yearsParam)
		teamsFilter = filter_team_for_matches(matches,teamsParam)
		leaguesFilter = filter_league_for_matches(matches,leaguesParam)

		pageCount = math.ceil(len(matches)/24)

		startIndex = (pageNumber - 1) * 24
		endIndex = startIndex + 24
		matches = matches[startIndex:endIndex]

		#Serializing
		match_serializer = MatchSerializer(matches,many=True)
		team_serializer = TeamSerializer(team,many=False)
		

		return Response({
			"team": team_serializer.data,
			"matches": match_serializer.data,
			"yearFilter": yearsFilter,
			"teamFilter": teamsFilter,
			"leagueFilter": leaguesFilter,
			"pageCount": pageCount
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
				match=match)
			rating = 0
			if len(rating_object) > 0:
				rating = rating_object[0].rating

			tries = Try.objects.filter(match=match)
			try_serializer = TrySerializer(tries, many=True)

			matches = Match.objects.filter(Q(
				home_team__in=[match.home_team, match.away_team]) & Q(away_team__in=[match.home_team, match.away_team])).filter(error=0).order_by('-date')[:10]

			match_serializer = MatchSerializer(match, many=False)
			matches_serializer = MatchSerializer(matches, many=True)

			return Response({
				"match": match_serializer.data,
				"matches": matches_serializer.data,
				"rating": rating,
				"tries": try_serializer.data
			})


class RatingAPI(APIView):
	def post(self, request):

		body = json.loads(request.body.decode('utf-8'))
		
		if request.GET.get('type') == "match":
			
			newrating = MatchRating(
				match=Match.objects.filter(id=body['id'])[0], rating=body['rating'])
			newrating.save()
			
		elif request.GET.get('type') == "try":
			
			newrating = TryRating(
				try_obj=Try.objects.filter(id=body['id'])[0], rating=body['rating'])
			newrating.save()
			

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

		league = League.objects.filter(name__in=["Mitre 10","USA","Top 14","Aviva Premiership"])
		mitre_10_league = league[0]
		league_2 = league[1]
		top_14_league = League.objects.filter(name="Top 14")[0]
		league_4 = league[3]
		league_super = League.objects.filter(name="Super Rugby")[0]

		if match_id == 'undefined':
			match_object = Match.objects.filter(match_completely_processed=0,video_link_found=1,error=0).exclude(league_id=top_14_league).order_by('-date')[0]
			print(match_object)
		else:
			match_object = Match.objects.filter(id=match_id)[0]

		match_serializer = MatchSerializer(match_object, many=False)

		if str(match_object.home_team.league_id) != "Mitre 10":
			scoreboard_url = "https://www.espn.co.uk/rugby/scoreboard?date=" + str(match_object.date.year) + str("{:02d}".format(match_object.date.month)) + str("{:02d}".format(match_object.date.day))
			soup = make_soup(scoreboard_url)
			
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
			
			return Response({"players": players_sorted, "match": match_serializer.data})
		else:
			scoreboard_url = match_object.region_blocked + "/commentary"

			print(scoreboard_url)
			soup = make_soup(scoreboard_url)

			events = soup.findAll('div', {'class': 'event'})

			try_blocks = []
			player_dicts = []

			for event in events:
				if "Try" in event.text:
					try_blocks.append(event)

			for try_block in try_blocks:
				player_name = try_block.find('b').text.strip()
				time_cleaned = try_block.find('div', {'class', 'time'}).text.strip()[:-1]

				try:
					player_object = Player.objects.filter(name=player_name)[0]
				except:
					if "event-home" in try_block.get('class'):
						player_object = Player(name=player_name, team=match_object.home_team)
						player_object.save()
					else:
						player_object = Player(name=player_name, team=match_object.away_team)
						player_object.save()

				player_dict = {'player_name':player_name, 'time':time_cleaned, 'id':player_object.id}
				player_dicts.append(player_dict)
			
			players_sorted = sorted(player_dicts, key=lambda k: int(k['time']))
			
			return Response({"players": players_sorted, "match": match_serializer.data})
		return


class AddTryAPI(APIView):
	def post(self, request):
		body = json.loads(request.body.decode('utf-8'))

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

class MatchesAPI(APIView):
	def get(self, request):

		order = request.GET.get('order')
		pageNumber = int(request.GET.get('page'))
		yearsParam = request.GET.get('year').split(",")
		teamsParam = request.GET.get('team').split(",")
		leaguesParam = request.GET.get('league').split(",")

		matches = Match.objects.filter(error=0)

		# Ordering
		if order == "date":
			matches = matches.order_by('-date')
		elif order == "rating":
			matches = matches.order_by('-ratings_average')

		#Filter information for querying database
		matches = query_year_for_matches(matches,yearsParam)    
		matches = query_team_for_matches(matches,teamsParam)
		matches = query_league_for_matches(matches,leaguesParam)

		# Filter information for front end
		yearsFilter = filter_year_for_matches(matches,yearsParam)
		teamsFilter = filter_team_for_matches(matches,teamsParam)
		leaguesFilter = filter_league_for_matches(matches,leaguesParam)
		print(leaguesFilter)

		pageCount = math.ceil(len(matches)/24)

		startIndex = (pageNumber - 1) * 24
		endIndex = startIndex + 24
		matches = matches[startIndex:endIndex]

		#Serializing
		match_serializer = MatchSerializer(matches,many=True)
		

		return Response({
			"matches": match_serializer.data,
			"yearFilter": yearsFilter,
			"teamFilter": teamsFilter,
			"leagueFilter": leaguesFilter,
			"pageCount": pageCount
		})

class TriesAPI(APIView):
	def get(self, request):

		order = request.GET.get('order')
		pageNumber = int(request.GET.get('page'))
		yearsParam = request.GET.get('year').split(",")
		teamsParam = request.GET.get('team').split(",")
		leaguesParam = request.GET.get('league').split(",")

		tries = Try.objects.filter(error=0)

		# Ordering
		if order == "date":
			tries = tries.order_by('-match__date')
		elif order == "rating":
			tries = tries.order_by('-ratings_average')

		#Filter information for querying database
		tries = query_year_for_tries(tries,yearsParam)    
		tries = query_team_for_tries(tries,teamsParam)
		tries = query_league_for_tries(tries,leaguesParam)


		# Filter information for front end
		yearsFilter = filter_year_for_tries(tries,yearsParam)
		teamsFilter = filter_team_for_tries(tries,teamsParam)
		leaguesFilter = filter_league_for_tries(tries,leaguesParam)

		pageCount = math.ceil(len(tries)/24)

		startIndex = (pageNumber - 1) * 24
		endIndex = startIndex + 24
		tries = tries[startIndex:endIndex]



		#Serializing
		try_serializer = TrySerializer(tries,many=True)
		

		return Response({
			"tries": try_serializer.data,
			"yearFilter": yearsFilter,
			"teamFilter": teamsFilter,
			"leagueFilter": leaguesFilter,
			"pageCount": pageCount
		})

class CompareTriesNZAPI(APIView):
	def get(self, request):


		start_date = datetime(2020, 6, 1)
		tries = Try.objects.filter(player__name="Jordie Barrett")

		try_a_random_int = random.randint(0, len(tries))
		try_b_random_int = random.randint(0,len(tries))

		try_a = tries[try_a_random_int]
		try_b = tries[try_b_random_int]


		#Serializing
		try_a_serializer = TrySerializer(try_a)
		try_b_serializer = TrySerializer(try_b)
		

		return Response({
			"try_a": try_a_serializer.data,
			"try_b": try_b_serializer.data,
		})

	def post(self, request):

		body = json.loads(request.body.decode('utf-8'))

		try_a = Try.objects.filter(id=body['try_a_id']).first()
		try_b = Try.objects.filter(id=body['try_b_id']).first()

		d = 0

		if body['try_a_id'] == body['winner']:
			d = 1
		else:
			d = 2

		Ra = try_a.elo_rating
		Rb = try_b.elo_rating
		K = 30

		new_ratings = EloRating(Ra, Rb, K, d)
		
		try_a.elo_rating = new_ratings[0]
		try_b.elo_rating = new_ratings[1]

		try_a.save()
		try_b.save()

		return Response(None)

class CompareTriesAPI(APIView):
	def get(self, request):

		tries = Try.objects.filter(error=0, match__date__year=2020)
				
		games_unrated = len(Try.objects.filter(error=0,elo_rating=1000))
		try_a_random_int = random.randint(0, len(tries))
		try_b_random_int = random.randint(0,len(tries))

		try_a = tries[try_a_random_int]
		try_b = tries[try_b_random_int]


		#Serializing
		try_a_serializer = TrySerializer(try_a)
		try_b_serializer = TrySerializer(try_b)
		

		return Response({
			"try_a": try_a_serializer.data,
			"try_b": try_b_serializer.data,
			"games_unrated": games_unrated,
		})

	def post(self, request):

		body = json.loads(request.body.decode('utf-8'))

		try_a = Try.objects.filter(id=body['try_a_id']).first()
		try_b = Try.objects.filter(id=body['try_b_id']).first()

		d = 0
		multiply_score_a = 1
		multiply_score_b = 1

		if body['try_a_id'] == body['winner']:
			d = 1

			if body['instagram_worthy']:
				if not Instagram.objects.filter(try_obj__id=body['try_a_id']).exists():
					instagram_queue = Instagram(try_obj=try_a, has_posted=False)
					instagram_queue.save()

				multiply_score_a = 2
		else:
			d = 2

			if body['instagram_worthy']:
				if not Instagram.objects.filter(try_obj__id=body['try_b_id']).exists():
					instagram_queue = Instagram(try_obj=try_b, has_posted=False)
					instagram_queue.save()

				multiply_score_b = 2

		Ra = try_a.elo_rating
		Rb = try_b.elo_rating
		K = 30

		new_ratings = EloRating(Ra, Rb, K, d)
		
		try_a.elo_rating = new_ratings[0] * multiply_score_a
		try_b.elo_rating = new_ratings[1] * multiply_score_b

		try_a.save()
		try_b.save()

		return Response(None)

class TriesLeaderboardAPI(APIView):
	def get(self, request):

		tries = Try.objects.all().order_by('-elo_rating')[:100]

		try_serializer = TrySerializer(tries,many=True)

		return Response({
			"tries": try_serializer.data,
		})

class TriesLeaderboardNZAPI(APIView):
	def get(self, request):

		start_date = datetime(2020, 6, 1)

		tries = Try.objects.filter(player__name="Jordie Barrett").order_by('-elo_rating')

		try_serializer = TrySerializer(tries,many=True)

		return Response({
			"tries": try_serializer.data,
		})

# Python 3 program for Elo Rating 
import math 
  
# Function to calculate the Probability 
def Probability(rating1, rating2): 
  
	return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 
  
  
# Function to calculate Elo rating 
# K is a constant. 
# d determines whether 
# Player A wins or Player B.  
def EloRating(Ra, Rb, K, d): 
   
  
	# To calculate the Winning 
	# Probability of Player B 
	Pb = Probability(Ra, Rb) 
  
	# To calculate the Winning 
	# Probability of Player A 
	Pa = Probability(Rb, Ra) 
  
	# Case -1 When Player A wins 
	# Updating the Elo Ratings 
	if (d == 1) : 
		Ra = Ra + K * (1 - Pa) 
		Rb = Rb + K * (0 - Pb) 
	  
  
	# Case -2 When Player B wins 
	# Updating the Elo Ratings 
	else : 
		Ra = Ra + K * (0 - Pa) 
		Rb = Rb + K * (1 - Pb)
		
	return [round(Ra, 6), round(Rb, 6)]
	

class InstagramAPI(viewsets.ViewSet):
	
	@action(methods=['post'], detail=False)
	def add_to_queue(self, request):

		body = json.loads(request.body.decode('utf-8'))

		try_obj = Try.objects.filter(id=body['id']).first()

		if not Instagram.objects.filter(try_obj__id=body['id']).exists():
			instagram_queue = Instagram(try_obj=try_obj, has_posted=False)
			instagram_queue.save()

		return Response(None)

	def posted_to_instagram(self, request):

		body = json.loads(request.body.decode('utf-8'))

		try_obj = Try.objects.filter(id=body['id']).first()

		if not Instagram.objects.filter(try_obj__id=body['id']).exists():
			instagram_queue = Instagram(try_obj=try_obj, has_posted=False)
			instagram_queue.save()

		return Response(None)
	  
	  
  



