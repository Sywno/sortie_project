from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    friends = models.ManyToManyField('self', blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    other_profile_field = models.CharField(max_length=100, blank=True, null=True)  # Exemple de champ supplémentaire

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

class GroupeAmis(models.Model):
    nom = models.CharField(max_length=100)
    createur = models.ForeignKey(User, related_name='groupes_crees', on_delete=models.CASCADE)
    membres = models.ManyToManyField(User, related_name='groupes_amis')

    def __str__(self):
        return self.nom

class Message(models.Model):
    groupe = models.ForeignKey(GroupeAmis, on_delete=models.CASCADE, related_name='messages')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoye = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.utilisateur.username}: {self.contenu[:20]}'

class SortieProposee(models.Model):
    groupe = models.ForeignKey(GroupeAmis, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    lieu = models.CharField(max_length=100)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='sorties_participants', through='Participation')

class Participation(models.Model):
    sortie = models.ForeignKey(SortieProposee, on_delete=models.CASCADE)
    membre = models.ForeignKey(User, on_delete=models.CASCADE)
    vient = models.BooleanField(default=False)  # Ajouter une valeur par défaut
