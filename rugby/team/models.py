from django.db import models

class Team(models.Model):
    name = models.TextField(default="")
    scraping_name = models.TextField(default="")

    def __str__(self):
        return self.name