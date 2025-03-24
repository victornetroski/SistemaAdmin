from django.contrib import admin
from .models import Comprobante, Emisor, Receptor, Concepto, Traslado, Impuestos, Complemento

# Registrar los modelos en el admin

admin.site.register(Emisor)
admin.site.register(Receptor)
admin.site.register(Concepto)
admin.site.register(Traslado)
admin.site.register(Impuestos)
admin.site.register(Complemento)

@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'total', 'tipo_comprobante')  # Campos que se mostrarán en la tabla
    search_fields = ('folio')  # Campos que se pueden buscar
    list_filter = ('forma_pago', 'tipo_comprobante')  # Filtros disponibles

