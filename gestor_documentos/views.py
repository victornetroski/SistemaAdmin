from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Documento, Asegurado
from .forms import DocumentoForm
from gestor_xml.views import procesar_xml
import xml.etree.ElementTree as ET
import os

# Create your views here.

@login_required
def principal(request):
    return render(request, 'gestor_documentos.html')

@login_required
def lista_asegurados(request):
    asegurados = Asegurado.objects.filter(usuario=request.user)
    return render(request, 'gestor_documentos/lista_asegurados.html', {
        'asegurados': asegurados
    })

@login_required
def agregar_asegurado(request):
    if request.method == 'POST':
        try:
            asegurado = Asegurado.objects.create(
                nombre=request.POST['nombre'],
                apellido_paterno=request.POST['apellido_paterno'],
                apellido_materno=request.POST['apellido_materno'],
                email=request.POST['email'],
                telefono=request.POST['telefono'],
                usuario=request.user
            )
            messages.success(request, 'Asegurado agregado exitosamente.')
            return redirect('lista_asegurados')
        except Exception as e:
            messages.error(request, f'Error al agregar asegurado: {str(e)}')
    
    return render(request, 'gestor_documentos/agregar_asegurado.html')

@login_required
def detalle_asegurado(request, asegurado_id):
    asegurado = get_object_or_404(Asegurado, id=asegurado_id, usuario=request.user)
    documentos = Documento.objects.filter(asegurado=asegurado)
    return render(request, 'gestor_documentos/detalle_asegurado.html', {
        'asegurado': asegurado,
        'documentos': documentos
    })

@login_required
def subir_documento(request, asegurado_id=None):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.usuario = request.user
            
            if asegurado_id:
                try:
                    asegurado = Asegurado.objects.get(id=asegurado_id, usuario=request.user)
                    documento.asegurado = asegurado
                except Asegurado.DoesNotExist:
                    messages.error(request, 'Asegurado no encontrado.')
                    return redirect('principal')
            
            # Verificar si es un archivo XML
            if documento.archivo.name.lower().endswith('.xml'):
                try:
                    # Procesar el XML
                    root, datos = procesar_xml(documento.archivo)
                    if root is not None:
                        documento.es_xml = True
                        documento.datos_xml = datos
                    else:
                        messages.error(request, 'Error al procesar el archivo XML.')
                        return redirect('principal')
                except Exception as e:
                    messages.error(request, f'Error al procesar el archivo XML: {str(e)}')
                    return redirect('principal')
            
            documento.save()
            messages.success(request, 'Documento subido exitosamente.')
            
            if asegurado_id:
                return redirect('detalle_asegurado', asegurado_id=asegurado_id)
            return redirect('principal')
    else:
        form = DocumentoForm()
    
    context = {
        'form': form,
        'asegurado_id': asegurado_id
    }
    return render(request, 'gestor_documentos/subir_documento.html', context)

@login_required
def ver_detalles_xml(request, documento_id):
    documento = Documento.objects.get(id=documento_id, usuario=request.user)
    
    try:
        # Procesar el XML
        root, datos = procesar_xml(documento.archivo)
        if root:
            return render(request, 'gestor_documentos/detalles_xml.html', {
                'documento': documento,
                'ns0_data': datos.get('ns0_data', []),
                'total': datos.get('total'),
                'uuid': datos.get('uuid')
            })
        else:
            messages.error(request, 'Error al procesar el XML.')
            return redirect('gestor_documentos')
    except Exception as e:
        messages.error(request, f'Error al procesar el XML: {str(e)}')
        return redirect('gestor_documentos')

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
