from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asegurado
from .forms import AseguradoForm
from django.http import FileResponse
import os

@login_required
def lista_asegurados(request):
    asegurados = Asegurado.objects.filter(usuario=request.user)
    return render(request, 'gestion_asegurados/lista_asegurados.html', {'asegurados': asegurados})

@login_required
def crear_asegurado(request):
    if request.method == 'POST':
        form = AseguradoForm(request.POST, request.FILES)
        if form.is_valid():
            asegurado = form.save(commit=False)
            asegurado.usuario = request.user
            asegurado.save()
            messages.success(request, 'Asegurado creado exitosamente.')
            return redirect('lista_asegurados')
    else:
        form = AseguradoForm()
    return render(request, 'gestion_asegurados/crear_asegurado.html', {'form': form})

@login_required
def detalle_asegurado(request, pk):
    asegurado = get_object_or_404(Asegurado, pk=pk, usuario=request.user)
    documentos = asegurado.documento_set.all()
    return render(request, 'gestion_asegurados/detalle_asegurado.html', {
        'asegurado': asegurado,
        'documentos': documentos
    })

@login_required
def editar_asegurado(request, pk):
    asegurado = get_object_or_404(Asegurado, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AseguradoForm(request.POST, request.FILES, instance=asegurado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asegurado actualizado exitosamente.')
            return redirect('detalle_asegurado', pk=pk)
    else:
        form = AseguradoForm(instance=asegurado)
    return render(request, 'gestion_asegurados/editar_asegurado.html', {'form': form})

@login_required
def eliminar_asegurado(request, pk):
    asegurado = get_object_or_404(Asegurado, pk=pk, usuario=request.user)
    if request.method == 'POST':
        asegurado.delete()
        messages.success(request, 'Asegurado eliminado exitosamente.')
        return redirect('lista_asegurados')
    return render(request, 'gestion_asegurados/eliminar_asegurado.html', {'asegurado': asegurado})

@login_required
def descargar_xml(request, pk):
    asegurado = get_object_or_404(Asegurado, pk=pk, usuario=request.user)
    if asegurado.archivo_xml:
        return FileResponse(asegurado.archivo_xml, as_attachment=True)
    messages.error(request, 'No hay archivo XML disponible.')
    return redirect('detalle_asegurado', pk=pk)
