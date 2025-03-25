from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Documento, Asegurado
from gestor_xml.views import procesar_xml, extract_ns0_elements, extract_total
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
def subir_documento(request):
    if request.method == 'POST':
        try:
            archivo = request.FILES['documento']
            descripcion = request.POST.get('descripcion', '')
            asegurado_id = request.POST.get('asegurado')
            
            # Verificar si el archivo es XML
            if archivo.name.lower().endswith('.xml'):
                try:
                    # Guardar el documento XML primero
                    documento = Documento.objects.create(
                        nombre=archivo.name,
                        archivo=archivo,
                        descripcion=descripcion,
                        usuario=request.user,
                        asegurado_id=asegurado_id
                    )
                    
                    # Procesar el XML
                    root = procesar_xml(documento.archivo)
                    if root:
                        # Extraer información del XML
                        ns0_data = extract_ns0_elements(root)
                        total = extract_total(ns0_data)
                        
                        # Redirigir a la vista de detalles del XML
                        return redirect('ver_detalles_xml', documento_id=documento.id)
                    else:
                        messages.error(request, 'Error al procesar el archivo XML.')
                        documento.delete()  # Eliminar el documento si hay error
                except ET.ParseError as e:
                    messages.error(request, f'Error al procesar el archivo XML: {str(e)}')
                    return render(request, 'gestor_documentos/subir_documento.html')
            else:
                # Si no es XML, guardar como documento normal
                documento = Documento.objects.create(
                    nombre=archivo.name,
                    archivo=archivo,
                    descripcion=descripcion,
                    usuario=request.user,
                    asegurado_id=asegurado_id
                )
                messages.success(request, 'Documento subido exitosamente.')
            
            return redirect('gestor_documentos')
        except Exception as e:
            messages.error(request, f'Error al subir el documento: {str(e)}')
    
    # Obtener lista de asegurados para el formulario
    asegurados = Asegurado.objects.filter(usuario=request.user)
    return render(request, 'gestor_documentos/subir_documento.html', {
        'asegurados': asegurados
    })

@login_required
def ver_detalles_xml(request, documento_id):
    documento = Documento.objects.get(id=documento_id, usuario=request.user)
    
    try:
        # Procesar el XML
        root = procesar_xml(documento.archivo)
        if root:
            # Extraer información
            ns0_data = extract_ns0_elements(root)
            total = extract_total(ns0_data)
            
            # Obtener el UUID del timbre fiscal
            namespaces = {'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
            timbre = root.find('.//tfd:TimbreFiscalDigital', namespaces)
            uuid = timbre.attrib.get('UUID') if timbre is not None else None
            
            return render(request, 'gestor_documentos/detalles_xml.html', {
                'documento': documento,
                'ns0_data': ns0_data,
                'total': total,
                'uuid': uuid
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
