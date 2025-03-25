from django.db import models
from django.contrib.auth.models import User

class Asegurado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    class Meta:
        ordering = ['-fecha_registro']

class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asegurado = models.ForeignKey(Asegurado, on_delete=models.CASCADE, null=True, blank=True)
    es_xml = models.BooleanField(default=False)
    datos_xml = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['-fecha_subida']
