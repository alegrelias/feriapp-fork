from django import forms
from .models import Feria,Categoria
from django.utils import timezone
from .models import Inscripcion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

        #  rango de puestos permitido a nivel formulario
        if 'capacidad_puestos' in self.fields:
            self.fields['capacidad_puestos'].widget.attrs.update({
                'placeholder': 'Minimo un puesto, máximo 100',
                'min': '1',
                'max': '100'
            })

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})

        self.fields['categoria'].widget.attrs.update({'class': 'form-select'})

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ["emprendedor", "feria", "numero_puesto", "estado", "registrado_por"]

        widgets = {
            'emprendedor': forms.Select(attrs={'class': 'form-select'}),
            'feria': forms.Select(attrs={'class': 'form-select'}),
            'numero_puesto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 14'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'registrado_por': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del operador'}),
        }

    def __init__(self, *args, **kwargs):
        feria_id = kwargs.pop('feria', None)
        emprendedor_id = kwargs.pop('emprendedor', None)

        super().__init__(*args, **kwargs)


        if feria_id and 'feria' in self.fields:
            self.initial['feria'] = feria_id

        if emprendedor_id and 'emprendedor' in self.fields:
            self.initial['emprendedor'] = emprendedor_id

        #aplicamos estilos y bloqueos
        for field_name, field in self.fields.items():
            if field_name == 'numero_puesto':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Ej: 14'
                })
            elif field_name == 'registrado_por':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Ej: Juan Pérez'
                })
            else:
                field.widget.attrs.update({
                    'readonly': 'readonly',
                    'class': 'form-control bg-light text-muted',
                    'style': 'pointer-events: none; cursor: not-allowed;',
                    'tabindex': '-1' #evita que el usuario llegue al campo usando la tecla TAB
                })


class RegistroEmprendedorForm(UserCreationForm):
    #forms.CharField → crea un <input type="text"> en el HTML y valida que no supere el max_length
    nombre = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    apellido = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    #ModelChoiceField se usa cuando el campo es una ForeignKey, en este caso rubro que apunta a Categoria. Genera un <select> con todas las categorías disponibles.
    rubro = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    password1 = forms.CharField(
        label="Contraseña",
         widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmà la contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }


class RegistroVisitanteForm(UserCreationForm):
    nombre = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    apellido = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Contraseña",
    widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmá la contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }
