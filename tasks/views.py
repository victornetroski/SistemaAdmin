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
from xml.etree.ElementTree import ParseError

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
        

def extract_moneda(root):
    moneda = None
    for child in root:
        # Verificar si 'Moneda' está en los atributos del nodo
        if "Moneda" in child.attrib:
            moneda = child.attrib["Moneda="]
            break  # Detener la búsqueda después de encontrar el primer resultado
    return moneda


@login_required
def upload_xml(request):
    if request.method == 'POST':
        try:
            form = XMLUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                
                # Validar si el archivo no está vacío
                if file.size == 0:
                    return HttpResponse("El archivo está vacío. Por favor, sube un archivo XML válido.", status=400)

                # Procesar el archivo XML
                tree = ET.parse(file)
                root = tree.getroot()

                # Extraer el dato de Moneda
                moneda = extract_moneda(root)

                # Generar un PDF mostrando el dato extraído
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="output.pdf"'

                pdf = canvas.Canvas(response)
                pdf.drawString(100, 750, "Dato extraído del XML:")
                pdf.drawString(100, 700, f"Moneda: {moneda or 'No encontrado'}")
                pdf.save()
                return response
        except ParseError:
            return HttpResponse("El archivo XML no es válido o está mal formado.", status=400)
        except Exception as e:
            logger.error(f"Error durante el procesamiento: {e}")
            return HttpResponse("Error en el servidor.", status=500)
    else:
        form = XMLUploadForm()

    return render(request, 'upload_xml.html', {'form': form})
