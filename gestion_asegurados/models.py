# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Compania(models.Model):
    id_aseguradora = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    nombre_corto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class AseguradoraPlan(models.Model):
    id_plan = models.AutoField(primary_key=True)
    id_aseguradora = models.ForeignKey(Compania, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id_aseguradora.nombre} - {self.nombre}"

class Poliza(models.Model):
    TIPO_CHOICES = [
        ('F', 'Fisica'),
        ('M', 'Moral'),
    ]
    
    id_poliza = models.AutoField(primary_key=True)
    id_aseguradora = models.ForeignKey(Compania, on_delete=models.CASCADE)
    id_plan = models.ForeignKey(AseguradoraPlan, on_delete=models.CASCADE)
    numero_poliza = models.CharField(max_length=100)
    fisica_moral = models.CharField(max_length=1, choices=TIPO_CHOICES)
    contratante_moral = models.CharField(max_length=255, blank=True, null=True)
    folio_mercantil = models.CharField(max_length=100, blank=True, null=True)
    objeto_social = models.TextField(blank=True, null=True)
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.CharField(max_length=255)
    curp = models.CharField(max_length=18)
    pais_nacimiento = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13)
    profesion = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    numero_exterior = models.CharField(max_length=50)
    numero_interior = models.CharField(max_length=50, blank=True, null=True)
    colonia = models.CharField(max_length=255)
    municipio_delegacion = models.CharField(max_length=255)
    entidad_federativa = models.CharField(max_length=255)
    ciudad_poblacion = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    poliza_pdf = models.FileField(upload_to='polizas/', blank=True, null=True)
    es_gobierno = models.BooleanField(default=False)
    cargo = models.CharField(max_length=255, blank=True, null=True)
    dependencia = models.CharField(max_length=255, blank=True, null=True)
    actua_nombre_propio = models.BooleanField(default=True)
    titular_contratante = models.CharField(max_length=255, blank=True, null=True)
    clabe = models.CharField(max_length=18, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    estado_cuenta_pdf = models.FileField(upload_to='estados_cuenta/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.numero_poliza} - {self.nombre} {self.apellido_paterno}"

class Asegurado(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    RELACION_CHOICES = [
        ('T', 'Titular'),
        ('C', 'Conyuge'),
        ('D', 'Dependiente'),
    ]

    id_asegurado = models.AutoField(primary_key=True)
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='O')
    rfc = models.CharField(max_length=13, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    relacion = models.CharField(max_length=50, choices=RELACION_CHOICES, default='T')
    iniciar_reclamo = models.BooleanField(default=False)
    diagnostico = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    class Meta:
        verbose_name = "Asegurado"
        verbose_name_plural = "Asegurados"
        ordering = ['-fecha_creacion']

class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(primary_key=True)
    id_asegurado = models.ForeignKey(Asegurado, on_delete=models.CASCADE, related_name='diagnosticos_asegurado')
    nombre = models.CharField(max_length=255)
    diagnostico = models.TextField()
    fecha_inicio_padecimiento = models.DateField()
    fecha_primera_atencion = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.id_asegurado}"

class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)
    cedula_profesional = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    telefono_consultorio = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido_paterno} - {self.especialidad}"

class InformeMedico(models.Model):
    id_informe = models.AutoField(primary_key=True)
    id_diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE)
    fecha_informe = models.DateField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='informes/')

    def __str__(self):
        return f"Informe {self.id_informe} - {self.id_diagnostico}"

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_reclamacion = models.CharField(max_length=100)
    archivo_pdf = models.FileField(upload_to='facturas/pdf/')
    archivo_xml = models.FileField(upload_to='facturas/xml/')
    archivo_desglose = models.FileField(upload_to='facturas/desglose/', blank=True, null=True)
    fecha = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=4)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=100)
    lugar_expedicion = models.CharField(max_length=255)
    nombre_emisor = models.CharField(max_length=255)
    rfc_emisor = models.CharField(max_length=13)
    domicilio_fiscal_receptor = models.CharField(max_length=255)
    nombre_receptor = models.CharField(max_length=255)
    rfc_receptor = models.CharField(max_length=13)
    uuid = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return f"Factura {self.id_factura} - {self.uuid}"

class PartidaFactura(models.Model):
    id_partida = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    descripcion = models.TextField()
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Partida {self.id_partida} - Factura {self.id_factura.id_factura}"