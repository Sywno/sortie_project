from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, FriendRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Sortie, Profile  # Assurez-vous d'importer Sortie ici


@login_required
def search_users(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query)).distinct()
    else:
        users = []
    return render(request, 'sorties/search_users.html', {'users': users})

@login_required
def send_friend_request(request, user_id):
    if request.user.id == user_id:
        messages.error(request, "Vous ne pouvez pas vous ajouter vous-même en ami.")
        return redirect('search_users')
    
    user = get_object_or_404(User, id=user_id)
    
    # Vérifier si une demande d'ami existe déjà
    friend_requests_sent = FriendRequest.objects.filter(from_user=request.user, to_user=user).exists()
    friend_requests_received = FriendRequest.objects.filter(from_user=user, to_user=request.user).exists()
    already_friends = request.user.profile.friends.filter(id=user.profile.id).exists()
    
    if friend_requests_sent or friend_requests_received:
        messages.info(request, f'Une demande d\'ami est déjà en attente avec {user.username}.')
    elif already_friends:
        messages.info(request, f'Vous êtes déjà amis avec {user.username}.')
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=user)
        messages.success(request, f'Demande d\'ami envoyée à {user.username}.')
    
    return redirect('search_users')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.profile.add_friend(friend_request.from_user.profile)
        friend_request.delete()
        messages.success(request, f'Vous avez accepté la demande d\'ami de {friend_request.from_user.username}.')
    return redirect('view_friends')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.info(request, f'Vous avez rejeté la demande d\'ami de {friend_request.from_user.username}.')
    return redirect('view_friends')

@login_required
def view_friends(request):
    profile = request.user.profile
    friends = profile.friends.all()
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'sorties/view_friends.html', {'friends': friends, 'friend_requests': friend_requests})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Votre compte a été créé ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'sorties/register.html', {'form': form})

def liste_sorties(request):
    sorties = Sortie.objects.all()
    return render(request, 'sorties/liste_sorties.html', {'sorties': sorties})

def creer_sortie(request):
    if request.method == 'POST':
        form = SortieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_sorties')
    else:
        form = SortieForm()
    return render(request, 'sorties/creer_sortie.html', {'form': form})
