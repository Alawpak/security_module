from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['login_usuario', 'nombre',
                    'fecha_inicio', 'fecha_fin', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('login_usuario', 'password')}),
        ('Información personal', {'fields': ('nombre', )}),
        ('Fecha inicio de sesion', {'fields': ('fecha_inicio', 'fecha_fin')}),
        ('Permisos', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'login_usuario', 'fecha_inicio', 'fecha_fin', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('login_usuario', 'nombre')
    ordering = ('login_usuario',)


# Registra el modelo de usuario personalizado con el administrador
admin.site.register(CustomUser, CustomUserAdmin)
