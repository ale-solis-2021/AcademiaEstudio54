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
    curso = models.ForeignKey('Course', on_delete=models.CASCADE)
    # movimiento = models.ForeignKey('Movimiento', on_delete=models.CASCADE)
    # inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombres} {self.apellido}"


# class Administracion(models.Model):
#     id_administracion = models.AutoField(primary_key=True)
#     nombre_usuario = models.CharField(max_length=255)
#     mail = models.EmailField(max_length=255)
#     password = models.CharField(max_length=255)
#     confirmacion = models.CharField(max_length=255)
#     fecha_de_registro = models.DateTimeField(auto_now_add=True)
#     usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.nombre_usuario


# class Curso(models.Model):
#     id_cursos = models.AutoField(primary_key=True)
#     nombre_del_curso = models.CharField(max_length=255)
#     descripcion = models.TextField()
#     fecha_inicio = models.DateField()
#     fecha_final = models.DateField()
#     duracion = models.IntegerField()
#     nivel = models.IntegerField()
#     importe_curso = models.DecimalField(max_digits=10, decimal_places=2)
#     materias = models.ForeignKey('Materia', on_delete=models.CASCADE)
#     materiales = models.ForeignKey('Material', on_delete=models.CASCADE)
#     condicion_curso = models.ForeignKey('CondicionCurso', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.nombre_del_curso


# class Profesor(models.Model):
#     id_profesor = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=255)
#     apellido = models.CharField(max_length=255)
#     correo_electronico = models.EmailField(max_length=255)
#     telefono = models.CharField(max_length=20)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.nombre} {self.apellido}"


# class Pago(models.Model):
#     id_pagos = models.AutoField(primary_key=True)
#     fecha = models.DateField()
#     numero_de_recibo = models.CharField(max_length=50)
#     descripcion = models.TextField()
#     cantidad_de_cuotas = models.IntegerField()
#     tarjeta = models.CharField(max_length=50)
#     vto_tarjeta = models.DateField()
#     banco = models.CharField(max_length=100)
#     importe_total = models.DecimalField(max_digits=10, decimal_places=2)
#     alumno = models.ForeignKey(ClienteAlumno, on_delete=models.CASCADE)
#     tipo_de_pago = models.IntegerField()
#     forma_pago = models.ForeignKey('EntidadFormaPago', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Pago {self.id_pagos}"


# class Materia(models.Model):
#     id_materias = models.AutoField(primary_key=True)
#     nombre_materia = models.CharField(max_length=255)
#     descripcion = models.TextField()
#     creditos = models.IntegerField()
#     profesor_responsable = models.ForeignKey(Profesor, on_delete=models.CASCADE)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.nombre_materia


# class Material(models.Model):
#     id_materiales = models.AutoField(primary_key=True)
#     titulo = models.CharField(max_length=255)
#     detalle = models.TextField()
#     fecha_subida = models.DateField()
#     autor = models.CharField(max_length=255)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
#     materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
#     tipo_formato = models.ForeignKey('TipoFormato', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.titulo


# class TipoFormato(models.Model):
#     id_tipo_formato = models.AutoField(primary_key=True)
#     campo_links = models.CharField(max_length=255)
#     campo_pdf = models.CharField(max_length=255)
#     campo_mp4 = models.CharField(max_length=255)
    
#     def __str__(self):
#         return f"Tipo Formato {self.id_tipo_formato}"


# class Calificacion(models.Model):
#     id_calificaciones = models.AutoField(primary_key=True)
#     fecha_evaluacion = models.DateField()
#     comentarios = models.TextField()
#     tipo_de_evaluacion = models.IntegerField()
#     peso_de_la_nota = models.DecimalField(max_digits=5, decimal_places=2)
#     nota = models.DecimalField(max_digits=5, decimal_places=2)
#     aprobado = models.BooleanField()
#     alumno = models.ForeignKey(ClienteAlumno, on_delete=models.CASCADE)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
#     materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Calificación {self.id_calificaciones}"


# class MovimientoFinanciacion(models.Model):
#     id_movim_financiacion = models.AutoField(primary_key=True)
#     fecha_cuota = models.DateField()
#     cuota = models.IntegerField()
#     vto_cuota = models.DateField()
#     importe_cuota = models.DecimalField(max_digits=10, decimal_places=2)
#     alumno = models.ForeignKey(ClienteAlumno, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Movimiento Financiación {self.id_movim_financiacion}"


# class EntidadFormaPago(models.Model):
#     id_forma_pago = models.AutoField(primary_key=True)
#     detalle = models.CharField(max_length=255)
#     tarjeta_credito_debito = models.BooleanField()
#     transferencia = models.BooleanField()
#     mercado_pago = models.BooleanField()
#     otros = models.BooleanField()
    
#     def __str__(self):
#         return self.detalle


# class CondicionCurso(models.Model):
#     id_condicion_curso = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=255)
#     detalle_condicion = models.TextField()
#     tipo = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.nombre


# class Movimiento(models.Model):
#     fecha_entrega_tarea = models.DateField()
#     fecha_movimiento = models.DateField()
#     tipo_movimiente = models.IntegerField()
#     usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE)
#     alumno = models.ForeignKey(ClienteAlumno, on_delete=models.CASCADE)
#     # profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
#     curso = models.ForeignKey(Course, on_delete=models.CASCADE)
#     # materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
#     # materiales = models.ForeignKey(Material, on_delete=models.CASCADE)
#     # movimiento = models.ForeignKey('self', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Movimiento {self.}"


# class TipoDeMovimiento(models.Model):
#     nombre_de_movimiento = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.nombre_de_movimiento


# class Inscripcion(models.Model):
#     id_inscripciones = models.AutoField(primary_key=True)
#     fecha_inscripcion = models.DateField()
#     importe_inscripcion = models.DecimalField(max_digits=10, decimal_places=2)
#     alumno = models.ForeignKey(ClienteAlumno, on_delete=models.CASCADE)
#     curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Inscripción {self.id_inscripciones}"
 