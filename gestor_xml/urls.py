from django.urls import path
from . import views

urlpatterns = [
    path('upload_xml/', views.upload_xml, name='upload_xml'),
]
