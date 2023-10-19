from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, login_usuario, password=None, **extra_fields):
        if not login_usuario:
            raise ValueError(
                'El campo de nombre de usuario debe ser proporcionado')
        user = self.model(login_usuario=login_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(login_usuario, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login_usuario = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido = models.CharField(max_length=30, blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    estado_cuenta = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Campos que estaban comentados
    # email = models.EmailField(unique=True)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)

    def is_login_allowed(self):

        now = timezone.now()

        if self.fecha_inicio and now < self.fecha_inicio:
            raise ValidationError('La cuenta aún no está activa.')

        if self.fecha_fin and now > self.fecha_fin:
            raise ValidationError('La cuenta ha expirado.')

        return True

    objects = CustomUserManager()

    USERNAME_FIELD = 'login_usuario'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def save(self, *args, **kwargs):
        # Agrega validaciones adicionales aquí antes de guardar
        self.is_login_allowed()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.login_usuario
