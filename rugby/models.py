from django.db import models
from django.contrib.contenttypes.fields import GenericRelation


def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


class League(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Team(models.Model):
    team_name = models.TextField()
    league = models.TextField(default='super')
    league_id = models.ForeignKey(League, on_delete=models.CASCADE, default=1)
    nationality = models.ForeignKey(
        'self', on_delete=models.CASCADE, default=2)
    logo = models.TextField()
    primary_colour = models.TextField(default='#000000')
    secondary_colour = models.TextField(default='#FFFFFF')

    def __str__(self):
        return self.team_name + "-" + str(self.id)


class Match(models.Model):
    date = models.DateTimeField()
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='away_team')
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    video_link = models.TextField()
    league = models.TextField(default='super')
    league_id = models.ForeignKey(League, on_delete=models.CASCADE)

    tries_created = models.IntegerField(default=0)

    video_link_found = models.IntegerField(default=0)
    video_downloaded = models.IntegerField(default=0)
    video_sliced = models.IntegerField(default=0)
    match_completely_processed = models.IntegerField(default=0)
    error = models.IntegerField(default=0)
    video_not_found = models.IntegerField(default=0)

    def avg_rating(self):
        ratings = MatchRating.objects.filter(match=self)
        sum = 0
        for rating in ratings:
            sum += rating.rating

        if len(ratings) > 0:
            return round(sum/len(ratings), 2)
        else:
            return 0

    def rating_count(self):
        ratings = MatchRating.objects.filter(match=self)
        return len(ratings)

    def __str__(self):
        return str(self.home_team.team_name) + " vs " + str(self.away_team.team_name) + " - " + str(self.date.date()) + " (" + str(self.match_completely_processed) + ")"


class PlayerManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Player(models.Model):
    name = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    internation_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='h', default=2)

    objects = PlayerManager()

    def __str__(self):
        return self.name + ' - ' + self.team.team_name

    def number_of_tries(self):
        tries = Try.objects.filter(player=self)
        return len(tries)


class Try(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, default=60)
    video_link = models.TextField()
    viewcount = models.IntegerField(default=1)
    ratings_average = models.IntegerField(default=2)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    ratings_average = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    error = models.IntegerField(default=0)

    def avg_rating(self):
        ratings = TryRating.objects.filter(try_obj=self)
        sum = 0
        for rating in ratings:
            sum += rating.rating

        if len(ratings) > 0:
            return round(sum/len(ratings), 2)
        else:
            return 0

    def rating_count(self):
        ratings = TryRating.objects.filter(try_obj=self)
        return len(ratings)

    def __str__(self):
        return str(self.player) + " in " + str(self.match)


class MatchRating(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    rating = models.IntegerField()
    userId = models.TextField()


class TryRating(models.Model):
    try_obj = models.ForeignKey(Try, on_delete=models.CASCADE)
    rating = models.IntegerField()
    userId = models.TextField()
