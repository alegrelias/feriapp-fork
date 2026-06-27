from django import forms
from .models import Inscripcion

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ["numero_puesto"]  # acá van los campos
