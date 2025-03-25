from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre', 'descripcion', 'archivo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        } 