from django.db import models
from django.contrib.auth.models import User

class XMLFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

from django.db import models

class Comprobante(models.Model):
    version = models.CharField(max_length=10)
    folio = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateTimeField()
    forma_pago = models.CharField(max_length=10, null=True, blank=True)
    no_certificado = models.CharField(max_length=50)
    certificado = models.TextField()
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    moneda = models.CharField(max_length=10, null=True, blank=True)
    exportacion = models.CharField(max_length=10, null=True, blank=True)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    tipo_comprobante = models.CharField(max_length=5, null=True, blank=True)
    metodo_pago = models.CharField(max_length=10, null=True, blank=True)
    lugar_expedicion = models.CharField(max_length=10, null=True, blank=True)
    sello = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Emisor(models.Model):
    comprobante = models.OneToOneField(Comprobante, on_delete=models.CASCADE, related_name='emisor')
    rfc = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    regimen_fiscal = models.CharField(max_length=10)

class Receptor(models.Model):
    comprobante = models.OneToOneField(Comprobante, on_delete=models.CASCADE, related_name='receptor')
    rfc = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    domicilio_fiscal = models.CharField(max_length=10, null=True, blank=True)
    regimen_fiscal_receptor = models.CharField(max_length=10)
    uso_cfdi = models.CharField(max_length=5)

class Concepto(models.Model):
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, related_name='conceptos')
    objeto_imp = models.CharField(max_length=5, null=True, blank=True)
    clave_prod_serv = models.CharField(max_length=20)
    no_identificacion = models.CharField(max_length=50, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    clave_unidad = models.CharField(max_length=10)
    unidad = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField()
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    importe = models.DecimalField(max_digits=15, decimal_places=2)

class Traslado(models.Model):
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE, related_name='traslados', null=True, blank=True)
    impuesto = models.CharField(max_length=10)
    base = models.DecimalField(max_digits=15, decimal_places=2)
    tipo_factor = models.CharField(max_length=20)
    tasa_o_cuota = models.DecimalField(max_digits=15, decimal_places=6)
    importe = models.DecimalField(max_digits=15, decimal_places=2)

class Impuestos(models.Model):
    comprobante = models.OneToOneField(Comprobante, on_delete=models.CASCADE, related_name='impuestos')
    total_trasladados = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

class Complemento(models.Model):
    comprobante = models.OneToOneField(Comprobante, on_delete=models.CASCADE, related_name='complemento')
    version = models.CharField(max_length=10)
    uuid = models.CharField(max_length=50, unique=True)
    fecha_timbrado = models.DateTimeField()
    rfc_prov_certif = models.CharField(max_length=20)
    sello_cfd = models.TextField()
    no_certificado_sat = models.CharField(max_length=50)
    sello_sat = models.TextField()
