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
    path('consultar_movimientos/', views.movimientos, name='movimientos'),
    path('movimiento/dashboard/', views.dashboard, name='dashboard'),
    path('movimiento/confirmar_eliminar_movimiento/<int:alumno_id>/', views.confirmar_eliminar_movimiento, name='confirmar_eliminar_movimiento'),
    path('movimiento/agregar_tarea/<int:alumno_id>/<int:curso_id>/<int:proyecto_id>', views.agregar_tarea, name='agregar_tarea'),
    path('movimiento/ver_actividad/<int:alumno_id>/', views.ver_actividad, name='ver_actividad'),
    path('movimiento/asignar_proyecto/<int:id_alumnos>', views.asignar_proyecto, name='asignar_proyecto'),
    path('movimiento/asignar_tarea/<int:id_alumnos>', views.asignar_tarea, name='asignar_tarea'),
    path('about/', views.about),
    path('inicio/', views.inicio),
    path('servicio/', views.servicios),
    path('contactos/', views.contactos),
]
