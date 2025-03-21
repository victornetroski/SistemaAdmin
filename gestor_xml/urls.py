from django.urls import path
from . import views

urlpatterns = [
    path('gestor_xml/', views.upload_xml, name='gestor_xml'),
    
]
