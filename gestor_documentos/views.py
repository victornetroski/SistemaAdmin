from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def principal(request):
    return render(request, 'gestor_documentos.html')

@login_required
def subir_documento(request):
    return render(request, 'gestor_documentos/subir_documento.html')

@login_required
def buscar_documento(request):
    return render(request, 'gestor_documentos/buscar_documento.html')
