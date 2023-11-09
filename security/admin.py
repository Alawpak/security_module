from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.urls import reverse


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


admin_site = CustomAdminSite(name='customadmin')
admin_site.register(Group)
admin_site.register(User)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
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
            'fields': ('nombre', 'login_usuario', 'fecha_inicio', 'fecha_fin', 'password1', 'password2', 'is_active'),
        }),
    )
    search_fields = ('login_usuario', 'nombre')
    ordering = ('login_usuario',)

    def response_add(self, request, obj, post_url_continue=None):
        if "_save" in request.POST:
            is_upcoming = obj.is_upcoming_date()
            is_start_date_after_end = obj.is_start_date_after_end()
            if is_upcoming:
                messages.error(
                    request, "La fecha del servidor es menor a la de inicio")
                return HttpResponseRedirect('/admin/security/customuser')
            if is_start_date_after_end:
                messages.error(
                    request, "La fecha de inicio no puede ser mayor a la de fin")
                return HttpResponseRedirect('/admin/security/customuser')
            else:
                return super().response_change(request, obj)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if "_save" in request.POST:
            is_upcoming = obj.is_upcoming_date()
            is_start_date_after_end = obj.is_start_date_after_end()
            if is_upcoming:
                messages.error(
                    request, "La fecha del servidor es menor a la de inicio")
                return HttpResponseRedirect('/admin/security/customuser')
            if is_start_date_after_end:
                messages.error(
                    request, "La fecha de inicio no puede ser mayor a la de fin")
                return HttpResponseRedirect('/admin/security/customuser')
            else:
                return super().response_change(request, obj)
        return super().response_change(request, obj)


admin.site = admin_site

# Registra el modelo de usuario personalizado con el administrador
admin.site.register(CustomUser, CustomUserAdmin)
