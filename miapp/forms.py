from django import forms
from .models import Project, Course, Task, ClienteAlumno, Movimiento, TipoMovimiento

class CreateNewTask(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), label="Proyecto Asociado")
    title = forms.CharField(label='Título de la Tarea', max_length=200)
    description = forms.CharField(label='Descripción de la Tarea:', widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ['title', 'description', 'project']

class CreateNewProject(forms.ModelForm): 
    # name = forms.CharField(label='Nombre del Proyecto: ', max_length=100)    
    # curso_id =forms.IntegerField(required=True, label="ID del curso")
    curso = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Asociado")
    class Meta:
            model = Project 
            fields = ['name', 'description','curso']  

class CreateNewAlumno(forms.ModelForm):
    curso = forms.ModelChoiceField(queryset=Course.objects.all(), label="Curso Asociado")
    
    class Meta:
        model = ClienteAlumno
        fields = ['nombres', 'apellido', 'dni', 'direccion', 'localidad', 'telefono', 'email', 'profesion', 'estudiante', 'curso']
    
class CreateNewCourse(forms.Form):
    name = forms.CharField(label='Nombre del Curso: ', max_length=100)
    description=forms.CharField(label='Descripcion del Curso:', widget=forms.Textarea)


class MovimientoForm(forms.ModelForm): 
    class Meta:
        model = Movimiento
        fields = ['tipo_movimiento', 'curso']  # Solo pedimos el curso y tipo de movimiento

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        
        # Traer todos los movimientos.object.all() 
        self.fields['tipo_movimiento'].queryset = TipoMovimiento.objects.all() 
    
        #Inicializar los atributos de los ClienteAlumno  
        self.fields['nombres'] = forms.CharField(label='Nombre: ', max_length=255)
        self.fields['apellido']  = forms.CharField(label='Apellido: ',max_length=255)
        self.fields['dni']  = forms.IntegerField(label='DNI: ')
        self.fields['direccion']  = forms.CharField(label='Direcciòn: ', max_length=255)
        self.fields['localidad']  = forms.CharField(label='Localidad: ', max_length=255)
        self.fields['telefono']  = forms.CharField(label='Telefono: ', max_length=20)
        self.fields['email']  = forms.EmailField(label='Email: ', max_length=255)
        self.fields['profesion']  = forms.CharField(label='Profesion: ', max_length=255)
   
   
   
class AsignacionProyectoForm(forms.Form):
    proyecto = forms.ModelChoiceField(queryset=Project.objects.all(), label="Proyecto Asociado ")
    def __init__(self, *args, **kwargs):
        alumno = kwargs.pop('alumno', None)  # Recibe el alumno como argumento
        super(AsignacionProyectoForm, self).__init__(*args, **kwargs)
        
        if alumno and alumno.curso:  # Verificamos si el alumno tiene un curso asociado
            # Filtrar proyectos que correspondan al curso del alumno
            self.fields['proyecto'].queryset = Project.objects.filter(curso=alumno.curso)
            print(f'Proyectos para el curso {alumno.curso}: {self.fields["proyecto"].queryset}')

class AsignacionTareaForm(forms.Form):
    tarea = forms.ModelChoiceField(queryset=Task.objects.all(), label="Tarea Asociada")
    
    def __init__(self, *args, **kwargs):
        alumno = kwargs.pop('alumno', None)
        super(AsignacionTareaForm, self).__init__(*args, **kwargs)
        
        if alumno and alumno.curso and alumno.proyecto:
            # Filtrar las tareas asociadas al proyecto del alumno
            self.fields['tarea'].queryset = Task.objects.filter(proyecto=alumno.proyecto)
            print(f'Tareas para el proyecto {alumno.proyecto}: {self.fields["tarea"].queryset}')

