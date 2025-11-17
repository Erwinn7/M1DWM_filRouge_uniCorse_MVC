from django import forms
from .models import Produit, Profil

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = '__all__'
        widgets = {
            'designation_p': forms.TextInput(attrs={'class': 'form-control'}),
            'type_p': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_ht': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_p': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['avatar', 'bio', 'phone', 'role']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
