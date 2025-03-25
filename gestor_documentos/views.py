from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Documento
from gestor_xml.views import procesar_xml, extract_ns0_elements, extract_total
import xml.etree.ElementTree as ET
import os

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
            
            # Verificar si el archivo es XML
            if archivo.name.lower().endswith('.xml'):
                try:
                    # Intentar parsear el XML
                    tree = ET.parse(archivo)
                    # Si es XML válido, procesarlo
                    root = procesar_xml(archivo)
                    if root:
                        # Extraer información del XML
                        ns0_data = extract_ns0_elements(root)
                        total = extract_total(ns0_data)
                        
                        # Guardar el documento XML
                        documento = Documento.objects.create(
                            nombre=archivo.name,
                            archivo=archivo,
                            descripcion=descripcion,
                            usuario=request.user
                        )
                        
                        # Redirigir a la vista de detalles del XML
                        return redirect('ver_detalles_xml', documento_id=documento.id)
                    else:
                        messages.error(request, 'Error al procesar el archivo XML.')
                except ET.ParseError as e:
                    messages.error(request, f'Error al procesar el archivo XML: {str(e)}')
                    return render(request, 'gestor_documentos/subir_documento.html')
            else:
                # Si no es XML, guardar como documento normal
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
def ver_detalles_xml(request, documento_id):
    documento = Documento.objects.get(id=documento_id, usuario=request.user)
    
    try:
        # Procesar el XML
        tree = ET.parse(documento.archivo)
        root = tree.getroot()
        
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
