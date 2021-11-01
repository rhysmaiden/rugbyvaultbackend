from rest_framework import serializers

from rugby.match.models import Match
from rugby.team.serializers import TeamSerializer

class MatchSerializer(serializers.ModelSerializer):

    home_team = TeamSerializer(many=False)
    away_team = TeamSerializer(many=False)

    class Meta:
        model = Match
        fields = ('avg_rating', 'rating_count', 'home_team', 'away_team',
                  'video_link', 'id', 'date')