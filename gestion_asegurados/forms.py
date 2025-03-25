from django import forms
from .models import Asegurado

class AseguradoForm(forms.ModelForm):
    class Meta:
        model = Asegurado
        fields = [
            'poliza', 'nombre', 'apellido_paterno', 
            'apellido_materno', 'fecha_nacimiento', 'genero', 'rfc', 
            'email', 'telefono', 'relacion', 
            'iniciar_reclamo', 'diagnostico'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'diagnostico': forms.Textarea(attrs={'rows': 4}),
        } 