from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UserChangeForm
from .models import CustomUser
from django.utils import timezone


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


class CustomPasswordChangeForm(PasswordChangeForm):
    show_password = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'show-password'}),
        label='Mostrar contraseñas'
    )


class PasswordInputWithToggle(forms.PasswordInput):
    template_name = 'admin/widgets/password_input_with_toggle.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Agregamos el tipo de widget al contexto
        context['widget']['type'] = 'password'
        return context


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña", widget=PasswordInputWithToggle(attrs={'type': 'password'}))

    class Meta:
        model = CustomUser
        fields = ('login_usuario', 'nombre', 'fecha_inicio',
                  'fecha_fin', 'password1', 'is_active')
        widgets = {
            'password1': forms.PasswordInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Quitamos el campo de confirmación de contraseña
        self.fields.pop('password2')

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        currentDate = timezone.localtime(timezone.now()).date()

        if fecha_inicio and fecha_inicio.date().day < currentDate.day:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser menor a la fecha del servidor.")
        elif fecha_inicio and fecha_inicio.date().day > currentDate.day:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser mayor a la del servidor")

        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                "La fecha fin no puede ser menor a la fecha inicio")

        return fecha_fin


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('login_usuario', 'password', 'nombre', 'fecha_inicio',
                  'fecha_fin', 'is_active', 'is_superuser', 'groups', 'user_permissions')

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        currentDate = timezone.localtime(timezone.now()).date()

        if fecha_inicio and fecha_inicio.date().day < currentDate.day:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser menor a la fecha del servidor.")
        elif fecha_inicio and fecha_inicio.date().day > currentDate.day:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser mayor a la del servidor")

        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                "La fecha fin no puede ser menor a la fecha inicio")

        return fecha_fin
