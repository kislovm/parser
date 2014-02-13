from django.db import models
from djangosphinx.models import SphinxSearch


class article(models.Model):
    article = models.TextField()
    url = models.CharField(max_length=300)
    search = SphinxSearch(
        mode= 'SPH_MATCH_ANY',
        rankmode= 'SPH_RANK_NONE',
        weights= { 'article': 100 }
    )

class Dictonary(models.Model):
    dict = models.TextField()
    name = models.CharField(max_length=100)
