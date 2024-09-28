from django.contrib import admin
from .models import Project, Task, Course,ClienteAlumno, TipoMovimiento,Movimiento, MovimientoTemporal

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Course)
admin.site.register(ClienteAlumno)
admin.site.register(TipoMovimiento)
admin.site.register(Movimiento)
admin.site.register(MovimientoTemporal)

# Register your models here.

