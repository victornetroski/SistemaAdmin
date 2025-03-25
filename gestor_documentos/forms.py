from django import forms
from .models import Documento, Asegurado

class AseguradoForm(forms.ModelForm):
    class Meta:
        model = Asegurado
        fields = [
            'id_asegurado', 'id_poliza', 'nombre', 'apellido_paterno', 
            'apellido_materno', 'fecha_nacimiento', 'genero', 'rfc', 
            'email', 'telefono', 'titulat_conyuge_dependiente', 
            'iniciar_reclamo', 'archivo_xml', 'diagnostico', 
            'numero_factura1', 'importe_factura1', 'dia1', 'dia2', 
            'mes1', 'mes2', 'año1', 'año2', 'año3', 'año4'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'diagnostico': forms.Textarea(attrs={'rows': 4}),
            'dia1': forms.NumberInput(attrs={'min': 1, 'max': 31}),
            'dia2': forms.NumberInput(attrs={'min': 1, 'max': 31}),
            'mes1': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'mes2': forms.NumberInput(attrs={'min': 1, 'max': 12}),
            'año1': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'año2': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'año3': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'año4': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'importe_factura1': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre', 'descripcion', 'archivo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        } 