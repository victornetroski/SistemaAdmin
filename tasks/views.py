from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import XMLUploadForm
import xml.etree.ElementTree as ET  # Para procesar XML
from reportlab.pdfgen import canvas  # Para generar PDFs
import logging
logger = logging.getLogger(__name__)
# Create your views here.

def home(request):

    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET' :
        return render(request, 'signup.html', {
                'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm, 
                    'error' : 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
              'form': UserCreationForm,
              'error': 'Las contraseñas no coinciden. Intenta nuevamente'
        
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'tasks.html', {'tasks':tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks.html', {'tasks':tasks})

@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
         })     
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html',{
                'form': TaskForm,
                'error': 'Proporciona datos validos'
         })     
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404 (Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html', {'task':task, 'form':form,
            'error': "Error al actualizar" })

@login_required       
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect ('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect ('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect("tasks")
        
@login_required
def upload_xml(request):
    if request.method == 'POST':
        try:
            form = XMLUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']

                # Procesar el archivo XML
                tree = ET.parse(file)
                root = tree.getroot()

                # Ejemplo: Obtener datos del XML
                data = []
                for child in root:
                    data.append(child.tag + ": " + child.text)

                # Generar un PDF con los datos extraídos
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="output.pdf"'

                pdf = canvas.Canvas(response)
                pdf.drawString(100, 750, "Datos extraídos del XML:")
                y = 700
                for line in data:
                    pdf.drawString(100, y, line)
                    y -= 20
                pdf.save()
                return response
        except Exception as e:
            logger.error(f"Error durante el procesamiento: {e}")
            return HttpResponse("Error en el servidor.", status=500)
    else:
        form = XMLUploadForm()

    return render(request, 'upload_xml.html', {'form': form})

