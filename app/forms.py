from django import forms
from .models import Feria
from django.utils import timezone

class FeriaForm(forms.ModelForm):

    class Meta:
        model = Feria

        fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos", "activa"]

        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date", "min": timezone.now().date().isoformat()}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['categoria'].empty_label = "Seleccione una categoría"

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})
        
        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})