from django.contrib import admin
from .models import GroupeAmis, Message, SortieProposee, Participation  # Ajoutez les nouveaux modèles

# Supprimez ou commentez la ligne suivante
# from .models import Sortie

# Enregistrez les nouveaux modèles dans l'admin
admin.site.register(GroupeAmis)
admin.site.register(Message)
admin.site.register(SortieProposee)
admin.site.register(Participation)