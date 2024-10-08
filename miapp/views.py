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
    title = 'Ver el listado de proyectos por curso'
    # Obtener todos los cursos con sus proyectos y tareas asociados
    courses = Course.objects.prefetch_related('project_set__task_set').all()

    return render(request, 'project/projects.html', {
        'title': title,
        'courses': courses,  # Pasamos los cursos en lugar de solo los proyectos
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
    # Obtener todos los cursos, y proyectos con sus respectivas tareas
    cursos = Course.objects.prefetch_related('project_set__task_set').all()

    return render(request, 'course/courses.html', {
        'courses': cursos
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
    if request.method == 'POST':
        form = CreateNewAlumno(request.POST)
        if form.is_valid():
            # Guardamos el alumno
            nuevo_alumno = form.save()

            # Crear un movimiento de tipo 'Inscripción'
            tipo_inscripcion = TipoMovimiento.objects.get(nombre="INSCRIPCION")  # Asegúrate de que el tipo exista
            Movimiento.objects.create(
                tipo_movimiento=tipo_inscripcion,
                alumno=nuevo_alumno,
                curso=nuevo_alumno.curso  # Relacionamos el curso del alumno
            )
            
            return redirect('crear_movimiento')  # Redirigir a la página de movimientos
    else:
        form = CreateNewAlumno()

    return render(request, 'movimiento/inscribir_alumno.html', {'form': form})
    
       
 
 
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

            # Filtrar proyectos que pertenecen al curso del alumno y están asignados por movimientos
            proyectos_asignados = Movimiento.objects.filter(
                alumno=alumno_seleccionado,
                tipo_movimiento__nombre='ASIGNACION DE PROYECTOS',
                proyecto__curso=curso  # Filtrar por curso del alumno
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



from django.shortcuts import redirect  # Import necesario para redirigir

def asignar_proyecto(request, id_alumnos):
    try:
        alumno = ClienteAlumno.objects.get(id=id_alumnos)
        tipo_movimiento = TipoMovimiento.objects.get(nombre='ASIGNACION DE PROYECTOS')
    except ClienteAlumno.DoesNotExist:
        return render(request, 'no_existe.html', {'id_alumnos': id_alumnos})

    # Obtener los movimientos del alumno para verificar su inscripción en cursos
    movimientos = Movimiento.objects.filter(alumno=alumno).select_related('curso', 'proyecto')

    # Consultar los proyectos disponibles para los cursos en los que está inscrito el alumno
    cursos_con_proyectos_y_tareas = {}

    for movimiento in movimientos:
        curso = movimiento.curso
        proyecto = movimiento.proyecto

        if curso not in cursos_con_proyectos_y_tareas:
            cursos_con_proyectos_y_tareas[curso] = {'proyectos': [], 'tareas': []}

        # Agregar el proyecto si pertenece al curso
        if proyecto and proyecto not in cursos_con_proyectos_y_tareas[curso]['proyectos']:
            cursos_con_proyectos_y_tareas[curso]['proyectos'].append(proyecto)

        # Obtener las tareas del proyecto
        if proyecto:
            tareas = Task.objects.filter(project=proyecto)
            cursos_con_proyectos_y_tareas[curso]['tareas'].extend(tareas)

    # Obtener los proyectos relacionados solo con los cursos en los que el alumno está inscrito
    cursos_inscritos = [movimiento.curso.id for movimiento in movimientos if movimiento.curso]

    # Filtrar proyectos que pertenezcan a los cursos inscritos y que aún no hayan sido asignados
    proyectos_disponibles = Project.objects.filter(curso__id__in=cursos_inscritos).exclude(
        id__in=[p.id for curso_data in cursos_con_proyectos_y_tareas.values() for p in curso_data['proyectos']]
    )

    # Guardar el movimiento si se ha enviado un proyecto seleccionado
    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto')
        if proyecto_id:
            proyecto = Project.objects.get(id=proyecto_id)
            curso = proyecto.curso  # Se asume que el proyecto ya está vinculado al curso

            # Crear un nuevo movimiento de asignación de proyecto
            nuevo_movimiento = Movimiento.objects.create(
                tipo_movimiento=tipo_movimiento,
                alumno=alumno,
                curso=curso,
                proyecto=proyecto
            )

            # Redirigir a la vista `consultar_movimientos` para mostrar el nuevo movimiento
            return redirect('consultar_movimientos', alumno_id=alumno.id)

    return render(request, 'movimiento/asignar_proyecto.html', {
        'alumno': alumno,
        'cursos_con_proyectos_y_tareas': cursos_con_proyectos_y_tareas,
        'proyectos_disponibles': proyectos_disponibles
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

def asignar_tarea(request, alumno_id, curso_id, proyecto_id):
    alumno = ClienteAlumno.objects.get(id=alumno_id)
    proyecto = Project.objects.get(id=proyecto_id)
    tareas = Task.objects.filter(project=proyecto)

    if request.method == 'POST':
        tarea_id = request.POST.get('tarea')
        tarea = Task.objects.get(id=tarea_id)

        # Crear el movimiento de asignación de tarea
        Movimiento.objects.create(
            tipo_movimiento='Asignar Tarea',
            alumno=alumno,
            curso_id=curso_id,
            proyecto=proyecto,
            tarea=tarea
        )
        return redirect('dashboard')

    return render(request, 'movimiento/asignar_tarea.html', {
        'alumno': alumno,
        'proyecto': proyecto,
        'tareas': tareas,
    })

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
    
def asignar_tarea_proyecto(request, alumno_id):
    alumno = ClienteAlumno.objects.get(id=alumno_id)
    cursos = Movimiento.objects.filter(alumno=alumno).values_list('curso', flat=True).distinct()
    
    proyectos = None
    tareas = None

    if request.method == 'POST':
        curso_id = request.POST.get('curso')  # Obtenemos el curso seleccionado
        proyecto_id = request.POST.get('proyecto')  # Obtenemos el proyecto seleccionado
        tarea_id = request.POST.get('tarea')  # Obtenemos la tarea seleccionada

        if curso_id and proyecto_id and tarea_id:
            curso = Course.objects.get(id=curso_id)
            proyecto = Project.objects.get(id=proyecto_id)
            tarea = Task.objects.get(id=tarea_id)

            # Crear un movimiento de tipo "Asignar Tarea"
            Movimiento.objects.create(
                tipo_movimiento="Asignar Tarea",
                alumno=alumno,
                curso=curso,
                proyecto=proyecto,
                tarea=tarea
            )

            return redirect('dashboard')  # Redirigir al dashboard o donde corresponda

        if curso_id:
            proyectos = Project.objects.filter(curso_id=curso_id)  # Filtramos los proyectos del curso
            tareas = Task.objects.filter(proyecto__curso_id=curso_id)  # Filtramos las tareas del curso

    return render(request, 'asignar_tarea_proyecto.html', {
        'alumno': alumno,
        'cursos': cursos,
        'proyectos': proyectos,
        'tareas': tareas,
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
def consultar_movimientos(request, alumno_id):
    try:
        alumno = ClienteAlumno.objects.get(id=alumno_id)
    except ClienteAlumno.DoesNotExist:
        return render(request, 'no_existe.html', {'alumno_id': alumno_id})

    # Obtener todos los movimientos del alumno
    movimientos = Movimiento.objects.filter(alumno=alumno).select_related('curso', 'proyecto', 'tarea')

    return render(request, 'movimiento/consultar_movimientos.html', {
        'alumno': alumno,
        'movimientos': movimientos
    })