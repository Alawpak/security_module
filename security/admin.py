# en admin.py de la aplicación 'security'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         ('Additional Information', {
#          'fields': ('telefono', 'fecha_inicio', 'fecha_fin')}),
#     )

# Muestra en la tabla de consulta
#     list_display = UserAdmin.list_display + ('telefono',)


# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Usuario)
