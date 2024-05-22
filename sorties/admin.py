# sortie_project/sorties/admin.py

from django.contrib import admin
from .models import Sortie

# Enregistrer le modèle Sortie dans l'admin
admin.site.register(Sortie)
