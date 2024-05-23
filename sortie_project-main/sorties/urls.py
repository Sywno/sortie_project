from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.liste_sorties, name='liste_sorties'),
    path('sorties/creer/', views.creer_sortie, name='creer_sortie'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='sorties/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='accueil'), name='logout'),  # Personnaliser la déconnexion    path('search_users/', views.search_users, name='search_users'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),  # Mettez à jour ce chemin
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('view_friends/', views.view_friends, name='view_friends'),
    path('accueil/', views.accueil, name='accueil'),
     path('search_users/', views.search_users, name='search_users'),  # Assurez-vous que ce chemin est bien défini
]
