from django import forms
from .models import *
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        exclude = ['vendedor', 'slug', 'published', 'pricing_tiers', 'ubicacion']
        
class InmuebleEditForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        exclude = ['vendedor', 'slug', 'published', 'pricing_tiers', 'ubicacion', 'image']
        
class UserCompleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['telefono', 'nombres', 'apellidos']