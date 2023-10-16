# from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# class CustomUser(AbstractUser):
#     telefono = models.CharField(max_length=15, blank=True, null=True)
#     fecha_inicio = models.DateTimeField(null=True, blank=True)
#     fecha_fin = models.DateTimeField(null=True, blank=True)

#     groups = models.ManyToManyField(
#         Group, related_name='customuser_set', blank=True)
#     user_permissions = models.ManyToManyField(
#         Permission, related_name='customuser_set', blank=True)


class Usuario(models.Model):
    cv_usuario = models.AutoField(primary_key=True)
    # django agrega al final _id si es una clave primaria, debe coincidir
    cv_nombre_id = models.ForeignKey(
        'Persona', on_delete=models.PROTECT, verbose_name='Persona', default="")
    login_usuario = models.CharField(max_length=255)
    pass_usuario = models.CharField(max_length=128)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_cuenta = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


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
