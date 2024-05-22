from django import forms
from .models import Sortie

class SortieForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'datepicker', 
        'id': 'id_date',
        'placeholder': 'YYYY-MM-DD'
    }))

    class Meta:
        model = Sortie
        fields = ['nom', 'description', 'date', 'lieu']
