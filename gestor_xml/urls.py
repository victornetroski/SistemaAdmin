from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_xml, name='upload_xml'),  # Página principal de tareas
    path('upload_xml/', views.upload_xml, name='upload_xml'),

    
]
