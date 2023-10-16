# Generated by Django 4.2.6 on 2023-10-16 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0010_catalogoaficiones_catalogoapellidosmaterno_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='cv_aficion',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='cv_ape_mat',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='cv_ape_pat',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='cv_direccion',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='cv_genero',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='cv_nombre',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='cv_tp_persona',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='cv_trabajo',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='cv_persona',
        ),
        migrations.DeleteModel(
            name='CatalogoAficiones',
        ),
        migrations.DeleteModel(
            name='CatalogoApellidosMaterno',
        ),
        migrations.DeleteModel(
            name='CatalogoApellidosPaterno',
        ),
        migrations.DeleteModel(
            name='CatalogoDirecciones',
        ),
        migrations.DeleteModel(
            name='CatalogoGeneros',
        ),
        migrations.DeleteModel(
            name='CatalogoNombres',
        ),
        migrations.DeleteModel(
            name='CatalogoTiposPersona',
        ),
        migrations.DeleteModel(
            name='CatalogoTrabajos',
        ),
        migrations.DeleteModel(
            name='Persona',
        ),
    ]
