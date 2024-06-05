# forms.py

from django import forms
from .models import GroupeAmis, SortieProposee, Participation, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class GroupeAmisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupeAmisForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['membres'].queryset = User.objects.filter(profile__in=user.profile.friends.all())

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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'other_profile_field']  # Ajoutez d'autres champs de profil ici
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Créer un profil uniquement s'il n'existe pas
            if not hasattr(user, 'profile'):
                profile = Profile(user=user, photo=self.cleaned_data['photo'])
                profile.save()
        return user
    
    
    
class AddMemberForm(forms.Form):
    membre = forms.ModelChoiceField(queryset=User.objects.all(), label="Ajouter un membre")