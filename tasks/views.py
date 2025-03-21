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
        
import xml.etree.ElementTree as ET

def procesar_xml(file):

    try:
        # Intentar cargar y analizar el archivo XML
        tree = ET.parse(file)  # Esto carga el archivo XML en un árbol
        root = tree.getroot()  # Obtiene la raíz del árbol

        print("Estructura del XML:", ET.tostring(root, encoding='utf-8').decode('utf-8'))

        # Si llega aquí, el XML se cargó correctamente
        print("XML cargado correctamente.")
        return root
    except ET.ParseError as e:
        # Capturar errores relacionados con el formato del XML
        print(f"Error en el formato del XML: {e}")
        return None
    except Exception as e:
        # Capturar otros errores genéricos
        print(f"Error inesperado: {e}")
        return None

        
def extract_comprobante_attributes(root):
    # Inicializar un diccionario para almacenar todos los atributos
    comprobante_attributes = {}

    # Definir el espacio de nombres (ajustar según el XML)
    namespaces = {'ns0': 'http://www.sat.gob.mx/cfd/4'}

    # Buscar el nodo Comprobante con el espacio de nombres
    comprobante_node = root.find('ns0:Comprobante', namespaces)
    if comprobante_node is not None:
        # Almacenar todos los atributos del nodo en un diccionario
        comprobante_attributes = comprobante_node.attrib

    return comprobante_attributes

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

                # Extraer los atributos del nodo <Comprobante>
                comprobante_attributes = extract_comprobante_attributes(root)

                # Depurar en consola
                print("Atributos extraídos del XML:", comprobante_attributes)

                # Generar un PDF mostrando los datos extraídos
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="output.pdf"'

                pdf = canvas.Canvas(response)
                pdf.drawString(100, 750, "Datos extraídos del XML:")

                # Iterar sobre los atributos y añadirlos al PDF
                y_position = 700  # Posición inicial en el eje Y
                if comprobante_attributes:
                    for key, value in comprobante_attributes.items():
                        pdf.drawString(100, y_position, f"{key}: {value}")
                        y_position -= 20  # Reducir la posición para la siguiente línea
                else:
                    pdf.drawString(100, y_position, "No se encontraron datos en el nodo Comprobante")

                pdf.save()
                return response
        except Exception as e:
            logger.error(f"Error durante el procesamiento: {e}")
            return HttpResponse("Error en el servidor.", status=500)
    else:
        form = XMLUploadForm()

    return render(request, 'upload_xml.html', {'form': form})
