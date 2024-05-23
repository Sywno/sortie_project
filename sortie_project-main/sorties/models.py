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
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

    def add_friend(self, profile):
        self.friends.add(profile)
        profile.friends.add(self)

    def remove_friend(self, profile):
        self.friends.remove(profile)
        profile.friends.remove(self)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'
