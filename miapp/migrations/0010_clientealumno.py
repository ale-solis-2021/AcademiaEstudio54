# Generated by Django 5.0.6 on 2024-09-02 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0009_remove_course_project_project_curso_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteAlumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('dni', models.IntegerField()),
                ('direccion', models.CharField(max_length=255)),
                ('localidad', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=255)),
                ('profesion', models.CharField(max_length=255)),
                ('estudiante', models.BooleanField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.course')),
            ],
        ),
    ]
