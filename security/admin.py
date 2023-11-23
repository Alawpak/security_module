from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.urls import reverse
from .forms import CustomUserCreationForm


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
