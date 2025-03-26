from django.urls import path
from . import views

app_name = 'gestion_asegurados'

urlpatterns = [
    path('', views.lista_asegurados, name='lista_asegurados'),
    path('crear/', views.crear_asegurado, name='crear_asegurado'),
    path('<int:pk>/', views.detalle_asegurado, name='detalle_asegurado'),
    path('<int:pk>/editar/', views.editar_asegurado, name='editar_asegurado'),
    path('<int:pk>/eliminar/', views.eliminar_asegurado, name='eliminar_asegurado'),
    path('<int:pk>/descargar-xml/', views.descargar_xml, name='descargar_xml'),
] 