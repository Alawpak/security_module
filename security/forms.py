# en forms.py de la aplicación 'security'
from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telefono', 'fecha_inicio', 'fecha_fin']  # Agrega 'phone' aquí