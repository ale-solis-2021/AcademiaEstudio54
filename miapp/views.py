#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Project, Task, Course, ClienteAlumno, Movimiento,TipoMovimiento,MovimientoTemporal
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask, CreateNewProject, CreateNewCourse,CreateNewAlumno, MovimientoForm, AsignacionProyectoForm, AsignacionTareaForm
from django.contrib import messages

# def hello(request, usuario):
#     print(usuario)
#     return render(f"Hello,!{usuario}")

# def hola(request):
#    return render(f"Holamundo")

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def inicio(request):
    return render(request, 'index.html')

def servicios(request):
    return render(request,'services.html')

def contactos(request):
    return render(request,'contacts.html')  

def projects(request):
    title ='ver el query set de proyecto'
    projects=Project.objects.all()
    print(projects)
    return render(request,'project/projects.html', {
        'title':  title,
        'projects': projects
        
    })
    
def create_project(request):
    c_cursos=Course.objects.all()
    print(c_cursos)

    if request.method == 'POST':

        form = CreateNewProject(request.POST)
        if form.is_valid():
            # en curso guardo la instancia completa, obtenemos la instancia (en este caso del curso seleccionado)
            curso = form.cleaned_data['curso']
            print('=====',curso)
            curso_id = curso.id 
            # Aquí guardas el ID del curso seleccionado
            # También puedes acceder al curso por su instancia completa
            print(f"Curso seleccionado: {curso.name}, ID: {curso_id}")

            # Guardar el proyecto usando form.save()
            project = form.save(commit=False)
            project.curso_id = curso_id
            project.save()

            return redirect('/projects/')
    else:
        form = CreateNewProject()

    context = {
        'curso': c_cursos,
        'form': form,
    }
    return render(request, 'project/create_project.html', context)
    
def alumnos(request):
    title = 'Listado de Alumnos'
    alumnos = ClienteAlumno.objects.all()
    return render(request, 'alumno/alumnos.html', {
        'title': title,
        'alumnos': alumnos
    })

def create_alumno(request):
    c_cursos = Course.objects.all()
    print(c_cursos)

    if request.method == 'POST':
        form = CreateNewAlumno(request.POST)
        if form.is_valid():
            curso = form.cleaned_data['curso']
            print('=====', curso)
            curso_id = curso.id
            print(f"Curso seleccionado: {curso.name}, ID: {curso_id}")

            alumno = form.save(commit=False)
            alumno.curso_id = curso_id
            alumno.save()

            return redirect('/alumnos/')
    else:
        form = CreateNewAlumno()

    context = {
        'curso': c_cursos,
        'form': form,
    }
    return render(request, 'alumno/create_alumno.html', context)

def tasks(request):
    
    tasks = Task.objects.all()
    return render(request, 'task/tasks.html', {
        'tasks': tasks
    })

    
def create_task(request):
    # Obtiene todos los proyectos para pasarlos al formulario
    c_proyectos = Project.objects.all()

    if request.method == 'POST':
        form = CreateNewTask(request.POST)
        if form.is_valid():
            # Obtén la instancia completa del proyecto seleccionado
            proyecto = form.cleaned_data['project']
            print('=====', proyecto)
            proyecto_id = proyecto.id
            # Guarda el ID del proyecto seleccionado
            print(f"Proyecto seleccionado: {proyecto.name}, ID: {proyecto_id}")

            # Guarda la tarea usando form.save()
            task = form.save(commit=False)
            task.project_id = proyecto_id
            task.save()

            return redirect('/tasks/')
    else:
        form = CreateNewTask()

    context = {
        'proyectos': c_proyectos,
        'form': form,
    }
    return render(request, 'task/create_task.html', context)

def listarTarea(request):
     courses = Course.objects.all()
     print(courses)
     return render(request, 'task/listarTarea.html',{
     'courses': courses    
     })


def courses(request):
    courses = Course.objects.all()
    return render(request,'course/courses.html' , {
        'courses': courses
    })
    
def create_course(request):
    if request.method == 'GET':
        return render(request, 'course/create_courses.html',{
            'form':CreateNewCourse()
            })
    else: 
        course = Course.objects.create(name=request.POST['name'], description=request.POST['description'])
        return redirect('/courses/')


def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            tipo_mov = form.cleaned_data['tipo_movimiento']
            print(tipo_mov.nombre)
            if tipo_mov.nombre != "INSCRIPCION":
                messages.error(request, 'Movimiento No Autorizado')
                return redirect('crear_movimiento')
            
            alumno = ClienteAlumno.objects.create(
                nombres = form.cleaned_data['nombres'],
                apellido=form.cleaned_data['apellido'],
                dni=form.cleaned_data['dni'],
                direccion=form.cleaned_data['direccion'],
                localidad=form.cleaned_data['localidad'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email'],
                profesion=form.cleaned_data['profesion'],
                curso=form.cleaned_data['curso'],
                estudiante=True
                
                
                
            )
            movimiento = form.save(commit=False) 
            movimiento.alumno = alumno
            movimiento.save()
            return redirect('/alumnos/')
          
            
    else:
        form = MovimientoForm()
    
    return render(request, 'movimiento/movimientos.html',{
            'form':form
            })       
 
 
def asignar_proyecto(request, id_alumnos):
    try:
        alumno = ClienteAlumno.objects.get(id = id_alumnos)
        tipo_movimiento = TipoMovimiento.objects.get(nombre = 'ASIGNACION DE PROYECTOS')
        print(alumno)
        curso = alumno.curso
    except:  
        print('El alumno no existe')
        return render(request, 'no_existe.html', {'id_alumnos': id_alumnos})
    
       
    if request.method == 'POST':
        form = AsignacionProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.cleaned_data['proyecto']
            print("Este es proyecto:",proyecto)
            print("Este es alumno: ",alumno)
            print("Este es curso",alumno.curso)
            print("id:", alumno.id, proyecto.id, curso.id, tipo_movimiento.id)
            movimiento_nuevo = Movimiento(
                 fecha_movimiento = timezone.now(),
                 tipo_movimiento = tipo_movimiento, 
                 alumno = alumno,
                 curso = curso,
                 proyecto = proyecto
            )
            movimiento_nuevo.save()
            return redirect('/alumnos/')
        
    else:     
        print('Voy a buscar los proyectos')
        form = AsignacionProyectoForm(request.POST, alumno = alumno)
        
    
    return render(request, 'movimiento/asignar_proyecto.html',{
            'form':form,
            'alumno':alumno
        })



def asignar_tarea(request, id_alumnos):
    alumno = ClienteAlumno.objects.get(id=id_alumnos)
    tipo_movimiento = TipoMovimiento.objects.get(nombre='ASIGNACION DE TAREAS')
    
    if request.method == 'POST':
        form = AsignacionTareaForm(request.POST)
        if form.is_valid():
            tarea = form.cleaned_data['task']
            curso = alumno.curso
            print(f"Tarea asignada: {tarea}")
            print(f"Alumno: {alumno}")
            print(f"Curso: {curso}")

            movimiento_nuevo = Movimiento(
                fecha_movimiento=timezone.now(),
                tipo_movimiento=tipo_movimiento,
                alumno=alumno,
                curso=curso,
                tarea=tarea
            )
            movimiento_nuevo.save()
            return redirect('/alumnos/')
    else:
        form = AsignacionTareaForm()

    return render(request, 'movimiento/asignar_tarea.html', {
        'form': form,
        'alumno': alumno
    })

def agregar_tarea(request, alumno_id, curso_id, proyecto_id):
    return render(request, 'movimiento/dashboard')

def movimientos(request):
    movimientos = Movimiento.objects.all().select_related('alumno','tipo_movimiento','curso','proyecto')
    print(movimientos)
    return render(request, 'movimiento/consultar_movimientos.html',{
        'movimientos':movimientos
    })
    
def llenar_tabla_temporal():
    # Limpiar la tabla temporal
    MovimientoTemporal.objects.all().delete()

    # Crear registros temporales
    movimientos = Movimiento.objects.select_related('alumno', 'curso', 'proyecto', 'tipo_movimiento').all()

    for movimiento in movimientos:
        tipo_movimiento_instance = movimiento.tipo_movimiento  # Obtener la instancia de TipoMovimiento

        MovimientoTemporal.objects.create(
            alumno_id=movimiento.alumno.id,
            alumno_nombre=f"{movimiento.alumno.nombres} {movimiento.alumno.apellido}",
            tipo_movimiento=tipo_movimiento_instance,  # Asignar la instancia
            curso_id=movimiento.curso.id if movimiento.curso else None,
            curso_name=movimiento.curso.name if movimiento.curso else None,
            proyecto_id=movimiento.proyecto.id if movimiento.proyecto else None,
            proyecto_name=movimiento.proyecto.name if movimiento.proyecto else None,
            fecha=movimiento.fecha_movimiento
        )

def dashboard(request):
    llenar_tabla_temporal()
    # Obtener todos los movimientos de la tabla temporal
    movimientos = MovimientoTemporal.objects.all()

    # Obtener todos los tipos de movimiento
    tipos_movimiento = TipoMovimiento.objects.all()

    # Si el usuario ha enviado un filtro de tipo de movimiento
    tipo_movimiento_id = request.GET.get('tipo_movimiento')

    if tipo_movimiento_id:
        # Filtrar los movimientos por el tipo de movimiento seleccionado
        movimientos = movimientos.filter(tipo_movimiento_id=tipo_movimiento_id)

    return render(request, 'movimiento/dashboard.html', {
        'movimientos': movimientos,
        'tipos_movimiento': tipos_movimiento,
    })
    
def dasAlumno(request):
    return

def confirmar_eliminar_movimiento(request, alumno_id):
    movimientoT = get_object_or_404(MovimientoTemporal, id=alumno_id)
    print('Mira lo que tengo en movimiento T')
    print(movimientoT)
    movimientos = None
    print("Fecha de movimiento Temporal:", movimientoT.fecha)
    original = movimientoT.fecha
    print("Fecha moviemiento original: ", original)
    try:
        movimientos = Movimiento.objects.filter(
            alumno_id = movimientoT.alumno_id, 
            curso_id = movimientoT.curso_id, 
            proyecto_id = movimientoT.proyecto_id,
            tipo_movimiento = movimientoT.tipo_movimiento_id,
            fecha = movimientoT.fecha
        )
        print('Encontrè el movimiento', movimientos)
    except Movimiento.DoesNotExist:
        print('No esta el movimiento en la tabla principal')
        return redirect('dashboard')  
    
    if request.method == 'POST':
        print('acà elimino los datos de la tabla temporal')   
        # MovimientoTemporal.delete()
        print("tengo que buscar los movimiento en la tabla original")
        
        return redirect('dashboard')
    
    context = {
        'movimiento':movimientoT
    }
    print('mostrar_formulario_con_los_registros')
    return render(request,'movimiento/confirmar_eliminar_movimiento.html', context)
   
    
# def tasks(request):
#     tarea=Task.objects.all()
#     print(tarea)
#     return HttpResponse("Tareas a desarrollar por los estudiantes")

#Funcion para obtener el Json de la los datos
# def tasks(request):
#     tarea=list(Task.objects.values())
#     print(tarea)
#     return JsonResponse(tarea, safe=False)

# def projects(request):
#     proyecto=list(Project.objects.values())
#     print(proyecto)
#     return JsonResponse(proyecto, safe=False)

# def courses(request):
#     curso=list(Course.objects.values())
#     print(curso)
#     return JsonResponse(curso, safe=False)


# def tasks(request, id):
#     # tarea=Task.objects.get(id=id)
#     tarea = get_object_or_404(Task, id = id)
#     return HttpResponse('Task : %s' % tarea.description)


# def proyects(request, id):
#     # tarea=Task.objects.get(id=id)
#     proyecto = get_object_or_404(Project, id = id)
#     return HttpResponse('Project : %s' % proyecto.name)

# def courses(request, id):
#     # tarea=Task.objects.get(id=id)
#     curso = get_object_or_404(Course, id = id)
#     return HttpResponse('Course : %s' % curso.name)
