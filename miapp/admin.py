from django.contrib import admin
from .models import Project, Task, Course,ClienteAlumno, TipoMovimiento

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Course)
admin.site.register(ClienteAlumno)
admin.site.register(TipoMovimiento)

# Register your models here.

