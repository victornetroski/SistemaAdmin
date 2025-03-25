from django.db import models
from django.contrib.auth.models import User

class Asegurado(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    id_asegurado = models.CharField(max_length=50, unique=True, null=True, blank=True)
    id_poliza = models.CharField(max_length=50, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='O')
    rfc = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    titulat_conyuge_dependiente = models.CharField(max_length=100, blank=True)
    iniciar_reclamo = models.BooleanField(default=False)
    archivo_xml = models.FileField(upload_to='xmls/', null=True, blank=True)
    diagnostico = models.TextField(blank=True)
    numero_factura1 = models.CharField(max_length=50, blank=True)
    importe_factura1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dia1 = models.IntegerField(null=True, blank=True)
    dia2 = models.IntegerField(null=True, blank=True)
    mes1 = models.IntegerField(null=True, blank=True)
    mes2 = models.IntegerField(null=True, blank=True)
    año1 = models.IntegerField(null=True, blank=True)
    año2 = models.IntegerField(null=True, blank=True)
    año3 = models.IntegerField(null=True, blank=True)
    año4 = models.IntegerField(null=True, blank=True)
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
