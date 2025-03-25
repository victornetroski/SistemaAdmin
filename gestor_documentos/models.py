from django.db import models
from django.contrib.auth.models import User

class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    descripcion = models.TextField(blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['-fecha_subida']
