from django.contrib import admin
from .models import Profile, FriendRequest, GroupeAmis, Message, SortieProposee, Participation

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(GroupeAmis)
admin.site.register(Message)
admin.site.register(SortieProposee)
admin.site.register(Participation)
