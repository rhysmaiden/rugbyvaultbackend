from django.db import models

from rugby.team.models import Team
from rugby.match.models import Match
from rugby.match.models import UserRating

class Trie(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=60)
    video_link = models.TextField()
    viewcount = models.IntegerField(default=1)
   
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)

    minute = models.IntegerField(default=0)
    error = models.IntegerField(default=0)

    # def avg_rating(self):
    #     ratings = TryRating.objects.filter(try_obj=self)
    #     sum = 0
    #     for rating in ratings:
    #         sum += rating.rating

    #     if len(ratings) > 0:
    #         ave = sum/len(ratings)
    #         self.ratings_average = ave
    #         self.save()
    #         return round(sum/len(ratings), 2)
    #     else:
    #         self.ratings_average = 0
    #         return 0

    # def rating_count(self):
    #     ratings = TryRating.objects.filter(try_obj=self)
    #     return len(ratings)

    def __str__(self):
        return str(self.player) + " in " + str(self.match)

class TrieRating(UserRating):
    trie = models.ForeignKey(Trie, on_delete=models.CASCADE)