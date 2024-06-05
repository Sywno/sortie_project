from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, FriendRequest, GroupeAmis, SortieProposee, Participation
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import GroupeAmisForm, SortieProposeeForm, ParticipationForm
from .forms import ProfileForm
from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import AddMemberForm


@login_required
def mes_evenements(request):
    # Get the groups the user belongs to
    user_groups = GroupeAmis.objects.filter(membres=request.user)

    # Get all events from those groups
    all_events = SortieProposee.objects.filter(groupe__in=user_groups).select_related('groupe')

    # Get user participations
    user_participations = Participation.objects.filter(membre=request.user, vient=True).select_related('sortie')

    # Create a dictionary to map events to participation status
    participation_status = {participation.sortie.id: 'Je participe' for participation in user_participations}

    context = {
        'all_events': all_events,
        'participation_status': participation_status
    }
    return render(request, 'sorties/mes_evenements.html', context)


@login_required
def toggle_participation(request, event_id):
    event = get_object_or_404(SortieProposee, id=event_id)
    participation, created = Participation.objects.get_or_create(membre=request.user, sortie=event)

    if participation.vient:
        participation.vient = False
        messages.success(request, f'Vous avez annulé votre participation à {event.nom}.')
    else:
        participation.vient = True
        messages.success(request, f'Vous participez maintenant à {event.nom}.')

    participation.save()
    return redirect('mes_evenements')

@login_required
def annuler_participation(request, participation_id):
    participation = get_object_or_404(Participation, id=participation_id, membre=request.user)
    if request.method == 'POST':
        participation.vient = False
        participation.save()
        messages.success(request, 'Vous avez annulé votre participation à cet événement.')
    return redirect('mes_evenements')

@login_required
def ajouter_membre(request, group_id):
    groupe = get_object_or_404(GroupeAmis, id=group_id)
    if request.user != groupe.administrateur:
        messages.error(request, "Vous n'êtes pas autorisé à ajouter des membres à ce groupe.")
        return redirect('groupe_detail', group_id=group_id)

    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            membre = form.cleaned_data['membre']
            groupe.membres.add(membre)
            messages.success(request, f'{membre.username} a été ajouté au groupe.')
            return redirect('groupe_detail', group_id=group_id)
    else:
        form = AddMemberForm()

    return render(request, 'sorties/ajouter_membre.html', {'groupe': groupe, 'form': form})

@login_required
def supprimer_membre(request, group_id, user_id):
    groupe = get_object_or_404(GroupeAmis, id=group_id)
    if request.user != groupe.administrateur:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer des membres de ce groupe.")
        return redirect('groupe_detail', group_id=group_id)

    membre = get_object_or_404(User, id=user_id)
    if membre == groupe.administrateur:
        messages.error(request, "Vous ne pouvez pas vous supprimer en tant qu'administrateur du groupe.")
    else:
        groupe.membres.remove(membre)
        messages.success(request, f'{membre.username} a été supprimé du groupe.')
    
    return redirect('groupe_detail', group_id=group_id)


@login_required
def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'sorties/view_profile.html', {'profile_user': profile_user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('view_profile', username=request.user.username)
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'sorties/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Les autres vues restent inchangées
@login_required
def proposer_sortie(request, group_id):
    groupe = get_object_or_404(GroupeAmis, id=group_id)
    if request.method == 'POST':
        form = SortieProposeeForm(request.POST)
        if form.is_valid():
            sortie = form.save(commit=False)
            sortie.groupe = groupe
            sortie.createur = request.user
            sortie.save()
            return redirect('groupe_detail', group_id=group_id)
    else:
        form = SortieProposeeForm()
    return render(request, 'sorties/proposer_sortie.html', {'form': form, 'groupe': groupe})



@login_required
def groupe_detail(request, group_id):
    groupe = get_object_or_404(GroupeAmis, id=group_id)
    sorties = SortieProposee.objects.filter(groupe=groupe)

    if request.method == 'POST':
        sortie_id = request.POST.get('form_id')
        vient = request.POST.get('vient') == 'True'
        sortie = get_object_or_404(SortieProposee, id=sortie_id)

        if vient:
            participation, created = Participation.objects.get_or_create(sortie=sortie, membre=request.user)
            participation.vient = True
            participation.save()
        else:
            Participation.objects.filter(sortie=sortie, membre=request.user).delete()

    participation_forms = {sortie.id: ParticipationForm() for sortie in sorties}
    
    return render(request, 'sorties/groupe_detail.html', {
        'groupe': groupe,
        'sorties': sorties,
        'participation_forms': participation_forms
    })

@login_required
def repondre_sortie(request, sortie_id):
    sortie = get_object_or_404(SortieProposee, id=sortie_id)
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.sortie = sortie
            participation.membre = request.user
            participation.save()
            return redirect('groupe_detail', group_id=sortie.groupe.id)
    else:
        form = ParticipationForm()
    return render(request, 'sorties/repondre_sortie.html', {'form': form, 'sortie': sortie})


@login_required
def creer_groupe(request):
    if request.method == 'POST':
        form = GroupeAmisForm(request.POST, user=request.user)
        if form.is_valid():
            groupe = form.save(commit=False)
            groupe.createur = request.user
            groupe.administrateur = request.user
            groupe.save()
            form.save_m2m()
            # Assurer que le créateur est membre après save_m2m()
            if request.user not in groupe.membres.all():
                groupe.membres.add(request.user)
            messages.success(request, 'Le groupe a été créé avec succès.')
            print(f"Groupe créé: {groupe.nom}, Membres: {[m.username for m in groupe.membres.all()]}")
            return redirect('liste_groupes')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = GroupeAmisForm(user=request.user)
    return render(request, 'sorties/creer_groupe.html', {'form': form})

@login_required
def liste_groupes(request):
    groupes = GroupeAmis.objects.filter(membres=request.user).prefetch_related('membres')
    for groupe in groupes:
        print(f'Groupe: {groupe.nom}, Membres: {[m.username for m in groupe.membres.all()]}')
    return render(request, 'sorties/liste_groupes.html', {'groupes': groupes})

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
    return render(request, 'sorties/view_friends.html', {
        'friends': friends,
        'friend_requests': friend_requests
    })
    

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('liste_groupes')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'sorties/register.html', {'form': form})

def accueil(request):
    return render(request, 'sorties/accueil.html')


def logout_view(request):
    logout(request)
    return redirect('accueil')