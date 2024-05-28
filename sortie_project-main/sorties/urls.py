from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.liste_groupes, name='liste_groupes'),
    path('sorties/creer/<int:group_id>/', views.proposer_sortie, name='creer_sortie'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='sorties/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='accueil'), name='logout'),
    path('search_users/', views.search_users, name='search_users'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('view_friends/', views.view_friends, name='view_friends'),
    path('accueil/', views.accueil, name='accueil'),
    path('creer_groupe/', views.creer_groupe, name='creer_groupe'),
    path('groupes/', views.liste_groupes, name='liste_groupes'),
    path('groupe/<int:group_id>/', views.groupe_detail, name='groupe_detail'),
    path('groupe/<int:group_id>/proposer_sortie/', views.proposer_sortie, name='proposer_sortie'),
    path('sortie/<int:sortie_id>/repondre/', views.repondre_sortie, name='repondre_sortie'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
]
