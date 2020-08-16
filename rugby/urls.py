from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.generic import ListView, DetailView
from rugby.models import Match
from rugby.models import Try
from rugby.models import Player
from rugby.models import Team

import itertools
from itertools import chain
from django.urls import path
# from rugby.views import TeamView
# from rugby.views import PlayerView
# from rugby.views import MatchView
# from rugby.views import LeagueView

from rest_framework import routers

from rest_framework.urlpatterns import format_suffix_patterns

# router = routers.DefaultRouter()
# router.register('highlights', views.Highlights, basename="players")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^highlights/$', views.Highlights.as_view()),
    url(r'^player/$', views.PlayerAPI.as_view()),
    url(r'^team/$', views.TeamAPI.as_view()),
    url(r'^video/$', views.VideoAPI.as_view()),
    url(r'^match/$', views.MatchHistoryAPI.as_view()),
    url(r'^rate/$', views.RatingAPI.as_view()),
    url(r'^chart/$', views.ChartAPI.as_view()),
    url(r'^search/$', views.SearchAPI.as_view()),
    url(r'^report/', views.ReportAPI.as_view()),
    url(r'^processing/', views.TryProcessingAPI.as_view()),
    url(r'^addtry/', views.AddTryAPI.as_view()),
    url(r'^matches/', views.MatchesAPI.as_view()),
    url(r'^tries/', views.TriesAPI.as_view()),
    url(r'^comparetries/', views.CompareTriesAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
