from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.liste_sorties, name='liste_sorties'),
    path('sorties/creer/', views.creer_sortie, name='creer_sortie'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='sorties/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='sorties/logout.html'), name='logout'),
]
