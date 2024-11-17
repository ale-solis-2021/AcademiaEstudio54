from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()   
    done = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.description}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)  
    
    def __str__(self):
        return f"{self.name} - {self.description} - {self.curso.name}"

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title + " " + self.description 

# class TipoDocumento(models.Model):
#     descripcion = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.descripcion


class ClienteAlumno(models.Model):
    nombres = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.IntegerField()
    direccion = models.CharField(max_length=255)
    localidad = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    profesion = models.CharField(max_length=255)
    estudiante = models.BooleanField()
    # tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    curso = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    # movimiento = models.ForeignKey('Movimiento', on_delete=models.CASCADE)
    # inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombres} {self.apellido}"



class TipoMovimiento(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    fecha_movimiento = models.DateTimeField(auto_now_add = True)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)
    # usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    alumno = models.ForeignKey(ClienteAlumno, on_delete=models.CASCADE)
    # profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    tarea = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)  
    hecho = models.BooleanField(default=False)
    
    # materiales = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.alumno}"


# Class Temporal para movimientos
class MovimientoTemporal(models.Model):
    alumno_id = models.IntegerField()
    alumno_nombre = models.CharField(max_length=255)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)  # Cambio aquí
    curso = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    curso_name = models.CharField(max_length=100, null=True, blank=True)
    proyecto = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    proyecto_name = models.CharField(max_length=100, null=True, blank=True)
    tarea_asignada = models.ForeignKey(Task,on_delete=models.CASCADE, null=True, blank=True, default=None)  # Campo para almacenar tareas asignadas
    fecha = models.DateTimeField()
    hecho = models.BooleanField(default=False)

    def __str__(self):
        return f"Alumno {self.alumno_nombre} - Movimiento {self.tipo_movimiento}"

# class Inscripcion(models.Model):
#     fecha_inscripcion = models.DateField()
#     importe_inscripcion = models.DecimalField(max_digits=10, decimal_places=2)
#     alumno = models.ForeignKey(ClienteAlumno, on_delete=models.CASCADE)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Inscripción {self.id_inscripciones}"
 