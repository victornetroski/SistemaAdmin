from django.contrib import admin
from .models import Comprobante, Emisor, Receptor, Concepto, Traslado, Impuestos, Complemento

# Registrar los modelos en el admin

admin.site.register(Comprobante)
admin.site.register(Emisor)
admin.site.register(Receptor)
admin.site.register(Concepto)
admin.site.register(Traslado)
admin.site.register(Impuestos)
admin.site.register(Complemento)
