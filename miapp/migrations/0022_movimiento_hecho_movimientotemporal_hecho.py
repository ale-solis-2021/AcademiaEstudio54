# Generated by Django 5.0.1 on 2024-10-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0021_movimientotemporal_tareas_asignadas'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='hecho',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movimientotemporal',
            name='hecho',
            field=models.BooleanField(default=False),
        ),
    ]
