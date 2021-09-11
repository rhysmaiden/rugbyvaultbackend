from django.contrib import admin
from rugby.match.models import *
from rugby.league.models import *
from rugby.team.models import *
from rugby.player.models import *
from rugby.trie.models import *
from rugby.rating.models import *
from rugby.instagram.models import *


class TrieAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)


class MatchAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    search_fields = ('home_team__team_name', 'away_team__team_name')
    # search_fields = ('league_id',)


class PlayerAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(ScrapedMatch)
admin.site.register(Match, MatchAdmin)
admin.site.register(ErrorMatch)
admin.site.register(MatchRating)

admin.site.register(Trie, TrieAdmin)
admin.site.register(TrieRating)

admin.site.register(Player, PlayerAdmin)

admin.site.register(League)

admin.site.register(Team)

admin.site.register(Instagram)
