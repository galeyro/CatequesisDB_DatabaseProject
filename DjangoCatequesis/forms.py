from django import forms
from .models import Alumno, Representante

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'nombre', 'apellido', 'fecha_nacimiento', 'lugar_nacimiento',
            'direccion', 'telefono_alumno', 'info_escolar', 'info_salud'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'apellido': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'direccion': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'telefono_alumno': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'info_escolar': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'info_salud': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }
        labels = {
            'info_escolar': 'Información Escolar',
            'info_salud': 'Información de Salud / Alergias',
        }

class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = ['nombre', 'apellido', 'telefono', 'email', 'ocupacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'apellido': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'ocupacion': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }
