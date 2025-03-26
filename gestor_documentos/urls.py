from django.urls import path
from . import views
from gestor_xml.views import generate_pdf
from django.contrib.auth.decorators import login_required

app_name = 'gestor_documentos'

urlpatterns = [
    path('', views.principal, name='principal'),
    path('gestor_documentos/', views.principal, name='gestor_documentos'),  # URL para el enlace en el template base
    path('subir-documento/', views.subir_documento, name='subir_documento'),  # URL para subir documento sin asegurado
    path('asegurados/<int:asegurado_id>/subir-documento/', views.subir_documento, name='subir_documento_asegurado'),
    path('asegurados/<int:asegurado_id>/generar-pdf/', login_required(generate_pdf), name='generate_pdf'),
    path('xml/<int:documento_id>/', views.ver_detalles_xml, name='ver_detalles_xml'),
    path('buscar/', views.buscar_documento, name='buscar_documento'),
] 