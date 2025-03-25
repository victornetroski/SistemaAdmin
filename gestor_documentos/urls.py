from django.urls import path
from . import views
from gestor_xml.views import generate_pdf
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.principal, name='principal'),
    path('gestor_documentos/', views.principal, name='gestor_documentos'),  # URL para el enlace en el template base
    path('asegurados/', views.lista_asegurados, name='lista_asegurados'),
    path('asegurados/agregar/', views.agregar_asegurado, name='agregar_asegurado'),
    path('asegurados/<int:asegurado_id>/', views.detalle_asegurado, name='detalle_asegurado'),
    path('asegurados/<int:asegurado_id>/subir-documento/', views.subir_documento, name='subir_documento'),
    path('asegurados/<int:asegurado_id>/generar-pdf/', login_required(generate_pdf), name='generate_pdf'),
    path('xml/<int:documento_id>/', views.ver_detalles_xml, name='ver_detalles_xml'),
    path('buscar/', views.buscar_documento, name='buscar_documento'),
] 