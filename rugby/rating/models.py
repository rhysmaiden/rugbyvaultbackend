from django.db import models

class UserRating(models.Model):
    rating = models.FloatField()

    class Meta:
        abstract = True