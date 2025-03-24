from django.urls import path
from . import views  # Importa las vistas de tu aplicación

urlpatterns = [
    path('upload_xml/', views.upload_xml, name='upload_xml'),  # Ruta para subir el XML
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),  # Ruta para generar el PDF
    path('gestor_xml/', views.upload_xml, name='gestor_xml'),  # Ruta para mostrar la página con los datos extraídos
]
