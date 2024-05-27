from django import forms
from .models import GroupeAmis, SortieProposee, Participation

class GroupeAmisForm(forms.ModelForm):
    class Meta:
        model = GroupeAmis
        fields = ['nom', 'membres']
        widgets = {
            'membres': forms.CheckboxSelectMultiple
        }

class SortieProposeeForm(forms.ModelForm):
    class Meta:
        model = SortieProposee
        fields = ['nom', 'description', 'date', 'lieu']


class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['vient']
