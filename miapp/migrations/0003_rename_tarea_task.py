# Generated by Django 5.0.6 on 2024-07-15 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0002_tarea'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tarea',
            new_name='task',
        ),
    ]
