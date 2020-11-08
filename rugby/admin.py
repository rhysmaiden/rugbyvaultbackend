from django.contrib import admin
from rugby.models import Match
from rugby.models import Player
from rugby.models import Try
from rugby.models import Team
from rugby.models import League
from rugby.models import Instagram
from rugby.models import MatchRating
from rugby.models import TryRating


class TryAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)


class MatchAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    search_fields = ('home_team__team_name', 'away_team__team_name')
    # search_fields = ('league_id',)


class PlayerAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Match, MatchAdmin)
admin.site.register(Team)
admin.site.register(MatchRating)
admin.site.register(TryRating)
admin.site.register(Player, PlayerAdmin)
admin.site.register(League)
admin.site.register(Try, TryAdmin)
admin.site.register(Instagram)
