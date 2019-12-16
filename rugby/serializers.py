from rest_framework import serializers
from.models import Player
from.models import Team
from.models import Match
from.models import Try
from.models import League


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


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
        model = Try
        fields = ('avg_rating', 'rating_count', 'player', 'match',
                  'video_link', 'id')


class HighlightSerializer(serializers.Serializer):
    matches = MatchSerializer(many=True)
    tries = TrySerializer(many=True)

# s
