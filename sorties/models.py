from django.db import models
from django.contrib.auth.models import User

class Sortie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='sorties')
    ...

class Groupe(models.Model):
    nom = models.CharField(max_length=100)
    membres = models.ManyToManyField(User, related_name='groupes')
    ...
