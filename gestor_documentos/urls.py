from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='gestor_documentos'),
    path('subir/', views.subir_documento, name='subir_documento'),
    path('buscar/', views.buscar_documento, name='buscar_documento'),
    path('xml/<int:documento_id>/', views.ver_detalles_xml, name='ver_detalles_xml'),
] 