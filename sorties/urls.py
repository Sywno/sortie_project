from django.urls import path
from . import views

urlpatterns = [
    path('sorties/', views.liste_sorties, name='liste_sorties'),
    path('sorties/creer/', views.creer_sortie, name='creer_sortie'),
]
