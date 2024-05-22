from django.shortcuts import render, redirect
from .models import Sortie
from .forms import SortieForm

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
