from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from sorties import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),  # Ajoutez cette ligne
    path('sorties/', include('sorties.urls')),
]
