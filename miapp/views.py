#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Project, Task, Course, ClienteAlumno
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask, CreateNewProject, CreateNewCourse,CreateNewAlumno, MovimientoForm

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
            
    else:
        form = MovimientoForm()
    
    return render(request, 'movimiento/movimiento.html',{
            'form':form
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
