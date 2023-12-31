from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


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
        extra_fields.setdefault('is_active', True)

        return self.create_user(login_usuario, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login_usuario = models.CharField(
        max_length=255, unique=True, blank=False, null=True)
    nombre = models.ForeignKey(
        'Persona', on_delete=models.PROTECT, blank=False, null=True, )
    fecha_inicio = models.DateTimeField(
        blank=False, null=True, default=timezone.now)
    fecha_fin = models.DateTimeField(blank=False, null=True)
    is_active = models.BooleanField(
        default=True, verbose_name="Cuenta activa")
    is_staff = models.BooleanField(default=True)

    def is_active_fun(self):
        if (self.is_active):
            return True
        return False

    def is_expirate_date(self):
        now = timezone.now()

        if self.fecha_fin and now > self.fecha_fin:
            return True
        return False

    def is_upcoming_date(self):
        currentDate = timezone.localtime(timezone.now()).date()

        if self.fecha_inicio and self.fecha_inicio.date().day < currentDate.day:
            return True
        return False

    def is_start_date_after_end(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            return True
        return False

    objects = CustomUserManager()

    USERNAME_FIELD = 'login_usuario'
    # REQUIRED_FIELDS = ['nombre']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.login_usuario


class CatalogoNombres(models.Model):
    cv_nombre = models.AutoField(primary_key=True)
    ds_nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_nombre


class CatalogoApellidosPaterno(models.Model):
    cv_ape_pat = models.AutoField(primary_key=True)
    ds_ape_pat = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_ape_pat


class CatalogoApellidosMaterno(models.Model):
    cv_ape_mat = models.AutoField(primary_key=True)
    ds_ape_mat = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_ape_mat


class CatalogoGeneros(models.Model):
    cv_genero = models.AutoField(primary_key=True)
    ds_genero = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_genero


class CatalogoTiposPersona(models.Model):
    cv_tp_person = models.AutoField(primary_key=True)
    ds_tp_person = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_tp_person


class CatalogoDirecciones(models.Model):
    cv_direccion = models.AutoField(primary_key=True)
    ds_direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_direccion


class CatalogoTrabajos(models.Model):
    cv_trabajo = models.AutoField(primary_key=True)
    ds_trabajo = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_trabajo


class CatalogoAficiones(models.Model):
    cv_aficion = models.AutoField(primary_key=True)
    ds_aficion = models.CharField(max_length=255)

    def __str__(self):
        return self.ds_aficion


class Persona(models.Model):
    cv_persona = models.AutoField(primary_key=True)
    cv_nombre = models.ForeignKey(
        'CatalogoNombres', on_delete=models.PROTECT, verbose_name='Nombre', default="")
    cv_ape_pat = models.ForeignKey(
        'CatalogoApellidosPaterno', on_delete=models.PROTECT, verbose_name='Apellido paterno', default="")
    cv_ape_mat = models.ForeignKey(
        'CatalogoApellidosMaterno', on_delete=models.PROTECT, verbose_name='Apellido materno', default="")
    cv_direccion = models.ForeignKey(
        'CatalogoDirecciones', on_delete=models.PROTECT, verbose_name='Direccion', default="")
    cv_genero = models.ForeignKey(
        'CatalogoGeneros', on_delete=models.PROTECT, verbose_name='Genero', default="")
    cv_trabajo = models.ForeignKey(
        'CatalogoTrabajos', on_delete=models.PROTECT, verbose_name='Trabajo', default="")
    cv_tp_persona = models.ForeignKey(
        'CatalogoTiposPersona', on_delete=models.PROTECT, verbose_name='Tipo de persona', default="")
    cv_aficion = models.ForeignKey(
        'CatalogoAficiones', on_delete=models.PROTECT, verbose_name='Aficion', null=True)
    telefono = models.CharField(
        max_length=15, blank=True, null=True, verbose_name='Telefono de la persona')
    email = models.EmailField(max_length=255, verbose_name='Email')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    notas = models.CharField(max_length=255, blank=True,
                             verbose_name='Notas de la persona')

    # podemos retornar concatenando cuando se use como llave foranea

    def __str__(self):
        return f'{self.cv_nombre.ds_nombre} {self.cv_ape_pat.ds_ape_pat} {self.cv_ape_mat.ds_ape_mat}'
