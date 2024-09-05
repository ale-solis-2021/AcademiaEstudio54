from django import forms
from .models import Project, Course, Task, ClienteAlumno

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
