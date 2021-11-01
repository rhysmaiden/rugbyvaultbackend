from rest_framework import serializers

from rugby.trie.models import Trie
from rugby.match.serializers import MatchSerializer
from rugby.player.serializers import PlayerSerializer


class TrieSerializer(serializers.ModelSerializer):

    player = PlayerSerializer(many=False)
    match = MatchSerializer(many=False)

    class Meta:
        model = Trie
        fields = ('avg_rating', 'rating_count', 'player', 'match',
                  'video_link', 'id', 'elo_rating', 'nz_elo_rating')