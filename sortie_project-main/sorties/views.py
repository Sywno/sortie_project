from django.shortcuts import render, redirect
from .models import Sortie
from .forms import SortieForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


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