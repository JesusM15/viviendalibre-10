from django import forms
from .models import *
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        exclude = ['vendedor', 'slug', 'published', 'pricing_tiers', 'ubicacion']
        
class InmuebleEditForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        exclude = ['vendedor', 'slug', 'published', 'pricing_tiers', 'ubicacion', 'image']