from rest_framework import serializers
from rugby.player.models import Player
from rugby.team.models import Team
from rugby.match.models import Match
from rugby.trie.models import Trie
from rugby.league.models import League


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id','name','team','internation_team','number_of_tries','number_of_int_tries')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):

    home_team = TeamSerializer(many=False)
    away_team = TeamSerializer(many=False)

    class Meta:
        model = Match
        fields = ('avg_rating', 'rating_count', 'home_team', 'away_team',
                  'video_link', 'id', 'date')


class TrySerializer(serializers.ModelSerializer):

    player = PlayerSerializer(many=False)
    match = MatchSerializer(many=False)

    class Meta:
        model = Trie
        fields = ('avg_rating', 'rating_count', 'player', 'match',
                  'video_link', 'id', 'elo_rating', 'nz_elo_rating')


class HighlightSerializer(serializers.Serializer):
    matches = MatchSerializer(many=True)
    tries = TrySerializer(many=True)

# s
