from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Documento

# Create your views here.

@login_required
def principal(request):
    return render(request, 'gestor_documentos.html')

@login_required
def subir_documento(request):
    if request.method == 'POST':
        try:
            archivo = request.FILES['documento']
            descripcion = request.POST.get('descripcion', '')
            
            documento = Documento.objects.create(
                nombre=archivo.name,
                archivo=archivo,
                descripcion=descripcion,
                usuario=request.user
            )
            
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('gestor_documentos')
        except Exception as e:
            messages.error(request, f'Error al subir el documento: {str(e)}')
    
    return render(request, 'gestor_documentos/subir_documento.html')

@login_required
def buscar_documento(request):
    documentos = Documento.objects.filter(usuario=request.user)
    busqueda = request.GET.get('busqueda', '')
    
    if busqueda:
        documentos = documentos.filter(
            nombre__icontains=busqueda
        ) | documentos.filter(
            descripcion__icontains=busqueda
        )
    
    return render(request, 'gestor_documentos/buscar_documento.html', {
        'documentos': documentos,
        'busqueda': busqueda
    })
