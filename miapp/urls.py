from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='index'),  
    path('tasks/', views.tasks),
    path('create_tasks/', views.create_task),
    path('listarTarea/', views.listarTarea),
    path('alumnos/', views.alumnos),
    path('create_alumno/', views.create_alumno),
    path('projects/', views.projects),
    path('create_project/', views.create_project),
    path('courses/', views.courses),
    path('create_courses/', views.create_course),
    path('movimientos/', views.crear_movimiento, name='crear_movimiento'),
    path('about/', views.about),
    path('inicio/', views.inicio),
    path('servicio/', views.servicios),
    path('contactos/', views.contactos),
]
