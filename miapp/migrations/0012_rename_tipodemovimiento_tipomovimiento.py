# Generated by Django 5.0.6 on 2024-09-07 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0011_tipodemovimiento_remove_clientealumno_curso_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TipoDeMovimiento',
            new_name='TipoMovimiento',
        ),
    ]
