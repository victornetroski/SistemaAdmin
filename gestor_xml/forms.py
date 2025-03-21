from django import forms
from .models import Task

class XMLUploadForm(forms.Form):
    file = forms.FileField(label="Subir archivo XML")