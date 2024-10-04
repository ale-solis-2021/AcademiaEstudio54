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
        #alta/ingreso alumno
            
            tipo_movimiento = TipoMovimiento.objects.get(nombre="INSCRIPCION")
            print(vars(tipo_movimiento))
            Movimiento.objects.create(
                alumno_id = alumno.id,
                curso_id = curso.id,
                tipo_movimiento_id = tipo_movimiento.id, 
                fecha_movimiento = timezone.now(),    
            )

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


# def crear_movimiento(request):
#     # obtener los datos del alumno  
#     alumnos = ClienteAlumno.objects.all()
#     alumno_seleccionado = None
#     proyectos_asignados = []
#     tareas_asignadas = [] 

#     if request.method == 'POST':
#         alumno_id = request.POST.get('alumno')
#         if alumno_id:
#             alumno_seleccionado = get_object_or_404(ClienteAlumno, id=alumno_id)
#             print(vars(alumno_seleccionado))
#             proyectos_asignados = Project.objects.filter(curso=alumno_seleccionado.curso)
#             tareas_asignadas = Task.objects.filter(project__curso=alumno_seleccionado.curso)
#         else:
#             return redirect('inscribir_alumno')

#     return render(request, 'movimiento/movimientos.html', {
#         'alumnos': alumnos,
#         'alumno_seleccionado': alumno_seleccionado,
#         'proyectos_asignados': proyectos_asignados,  
#         'tareas_asignadas': tareas_asignadas,  
#     })
 
    

def inscribir_alumno(request):
    return redirect('crear_movimiento')
    
       
 
 
def crear_movimiento(request):
    # Obtener todos los alumnos
    alumnos = ClienteAlumno.objects.all()
    alumno_seleccionado = None
    proyectos_asignados = []
    tareas_asignadas = []

    if request.method == 'POST':
        alumno_id = request.POST.get('alumno')

        if alumno_id:
            alumno_seleccionado = get_object_or_404(ClienteAlumno, id=alumno_id)

            # Obtener el curso del alumno
            curso = alumno_seleccionado.curso

            # Filtrar proyectos asignados por el movimiento del alumno
            proyectos_asignados = Movimiento.objects.filter(
                alumno=alumno_seleccionado,
                tipo_movimiento__nombre='ASIGNACION DE PROYECTOS'
            ).select_related('proyecto')

            # Filtrar tareas por los proyectos asignados al alumno
            proyectos_ids = proyectos_asignados.values_list('proyecto__id', flat=True)
            tareas_asignadas = Task.objects.filter(project__id__in=proyectos_ids)
        else:
            return redirect('inscribir_alumno')

    return render(request, 'movimiento/movimientos.html', {
        'alumnos': alumnos,
        'alumno_seleccionado': alumno_seleccionado,
        'proyectos_asignados': proyectos_asignados,
        'tareas_asignadas': tareas_asignadas,
    })



def asignar_proyecto(request, id_alumnos):
    try:
        alumno = ClienteAlumno.objects.get(id=id_alumnos)
        tipo_movimiento = TipoMovimiento.objects.get(nombre='ASIGNACION DE PROYECTOS')
    except ClienteAlumno.DoesNotExist:
        return render(request, 'no_existe.html', {'id_alumnos': id_alumnos})

    # Consultar los movimientos del alumno para obtener los cursos, proyectos y tareas
    movimientos = Movimiento.objects.filter(alumno=alumno)

    # Organizar los proyectos y tareas en función de los cursos
    cursos_con_proyectos_y_tareas = {}
    
    for movimiento in movimientos:
        curso = movimiento.curso
        proyecto = movimiento.proyecto
        tarea = movimiento.tarea

        if curso not in cursos_con_proyectos_y_tareas:
            cursos_con_proyectos_y_tareas[curso] = {'proyectos': {}, 'tareas': []}
        
        # Añadir proyectos a los cursos
        if proyecto and proyecto not in cursos_con_proyectos_y_tareas[curso]['proyectos']:
            cursos_con_proyectos_y_tareas[curso]['proyectos'][proyecto] = {'tareas': []}
        
        # Añadir tareas a los proyectos
        if tarea and proyecto:
            cursos_con_proyectos_y_tareas[curso]['proyectos'][proyecto]['tareas'].append(tarea)

    return render(request, 'movimiento/asignar_proyecto.html', {
        'alumno': alumno,
        'cursos_con_proyectos_y_tareas': cursos_con_proyectos_y_tareas
    })

def asignar_tarea(request, id_alumnos, proyecto_name):
    alumno = ClienteAlumno.objects.get(id=id_alumnos)
    tipo_movimiento = TipoMovimiento.objects.get(nombre='ASIGNACION DE TAREAS')
    proyecto = get_object_or_404(Project, name=proyecto_name)
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

    # Crear registros temporales obteniendo todos los movimientos
    movimientos = Movimiento.objects.select_related('alumno', 'curso', 'proyecto', 'tipo_movimiento').all()

    for movimiento in movimientos:
        tipo_movimiento_instance = movimiento.tipo_movimiento  # Obtener la instancia de TipoMovimiento

        # Obtener las tareas relacionadas con el proyecto si el proyecto existe
        tareas = Task.objects.filter(project_id=movimiento.proyecto.id) if movimiento.proyecto else None

        # Concatenar las tareas en un string o almacenarlas en la tabla temporal de la manera que prefieras
        tareas_asignadas = ', '.join([tarea.title for tarea in tareas]) if tareas else None

        # Crear el registro en la tabla temporal
        MovimientoTemporal.objects.create(
            alumno_id=movimiento.alumno.id,
            alumno_nombre=f"{movimiento.alumno.nombres} {movimiento.alumno.apellido}",
            tipo_movimiento=tipo_movimiento_instance,  # Asignar la instancia de TipoMovimiento
            curso_id=movimiento.curso.id if movimiento.curso else None,
            curso_name=movimiento.curso.name if movimiento.curso else None,
            proyecto_id=movimiento.proyecto.id if movimiento.proyecto else None,
            proyecto_name=movimiento.proyecto.name if movimiento.proyecto else None,
            tareas_asignadas=tareas_asignadas,  # Guardar las tareas asignadas como string
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
            fecha_movimiento = movimientoT.fecha
        )
        print('Encontrè el movimiento', movimientos)
    except Movimiento.DoesNotExist:
        print('No esta el movimiento en la tabla principal')
        return redirect('dashboard')  
    
    if request.method == 'POST':
        print('acà elimino los datos de la tabla temporal')   
        movimientoT.delete()
        print('movimiento tabla temporal eliminado')
        if movimientos.exists():
            for movi in movimientos:
                movi.delete()
            print('Los movimientos se eliminaron correctamente')
        else:        
            print("No encontrrè movimiento para eliminar")
        
        return redirect('dashboard')
    
    context = {
        'movimiento':movimientoT
    }
    print('mostrar_formulario_con_los_registros')
    return render(request,'movimiento/confirmar_eliminar_movimiento.html', context)

def ver_actividad(request, alumno_id):
    # Obtener el alumno por su ID
    alumno = get_object_or_404(ClienteAlumno, id=alumno_id)
    
    # Obtener todos los movimientos relacionados al alumno
    movimientos = Movimiento.objects.filter(alumno=alumno).order_by('fecha_movimiento')

    return render(request, 'movimiento/ver_actividad.html', {
        'alumno': alumno,
        'movimientos': movimientos
    })   
    
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
