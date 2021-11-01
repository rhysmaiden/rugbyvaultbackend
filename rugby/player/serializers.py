from rest_framework import serializers

from rugby.player.models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id','name','team','internation_team','number_of_tries','number_of_int_tries')
