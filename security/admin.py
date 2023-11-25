from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        # Obtener el nombre del usuario actual o mostrar un mensaje predeterminado si no está autenticado
        user = request.user
        if user.is_authenticated:
            self.site_header = f'Bienvenido, {user.nombre}'
        return super().index(request, extra_context)

    def password_change(self, request):
        change_password_url = reverse('change_password')
        return HttpResponseRedirect(change_password_url)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm  # Utiliza el formulario personalizado
    add_form_template = 'admin/add_form.html'
    # Use the default password change form
    form = CustomUserChangeForm

    def add_view(self, request, form_url='', extra_context=None):
        # Obtén todos los usuarios
        all_users = CustomUser.objects.all()

        # Pasa los usuarios al contexto
        extra_context = extra_context or {}
        extra_context['all_users'] = all_users

        #Si el profe quiere que se quede en la misma pagina
        # if request.method == 'POST':
        #     response = super().add_view(request, form_url, extra_context)
        #     # Redirige a la misma página
        #     response['Location'] = request.get_full_path()
        #     return response

        return super().add_view(request, form_url, extra_context)

    list_display = ['login_usuario', 'nombre',
                    'fecha_inicio', 'fecha_fin', 'is_active']
    fieldsets = (
        (None, {'fields': ('login_usuario', 'password')}),
        ('Información personal', {'fields': ('nombre', )}),
        ('Fecha inicio de sesion', {'fields': ('fecha_inicio', 'fecha_fin')}),
        ('Permisos', {'fields': ('is_active',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'login_usuario', 'fecha_inicio', 'fecha_fin', 'password1', 'is_active'),
        }),
    )
    search_fields = ('login_usuario', 'nombre')
    ordering = ('login_usuario',)


admin_site = CustomAdminSite(name='customadmin')
admin.site = admin_site

# Registra el modelo de usuario personalizado con el administrador

admin_site.register(Group)
admin_site.register(User)
admin.site.register(CustomUser, CustomUserAdmin)
