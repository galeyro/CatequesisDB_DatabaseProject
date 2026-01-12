from django import forms
from .models import Alumno, Representante, Grupo, Inscripcion, Parroquia, Nivel, Periodo

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
            'nombre': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'apellido': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'telefono': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'ocupacion': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
        }

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['id_parroquia', 'id_nivel', 'id_periodo']
        widgets = {
            'id_parroquia': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'id_nivel': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'id_periodo': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }
        labels = {
            'id_parroquia': 'Parroquia',
            'id_nivel': 'Nivel de Catequesis',
            'id_periodo': 'Periodo Lectivo'
        }

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['id_grupo', 'fecha_inscripcion', 'estado_inscripcion', 'comentarios_excepcion']
        widgets = {
            'id_grupo': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'fecha_inscripcion': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'estado_inscripcion': forms.Select(choices=[('Activo', 'Activo'), ('Retirado', 'Retirado')], attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'comentarios_excepcion': forms.Textarea(attrs={'rows': 3, 'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
        }

class ParroquiaForm(forms.ModelForm):
    class Meta:
        model = Parroquia
        fields = ['nombre_parroquia', 'direccion', 'telefono_secretaria']
        widgets = {
            'nombre_parroquia': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'direccion': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'telefono_secretaria': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
        }

class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = ['nombre_nivel', 'orden', 'sacramento_id_sacramento']
        widgets = {
            'nombre_nivel': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'orden': forms.NumberInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'sacramento_id_sacramento': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }
        labels = {
            'sacramento_id_sacramento': 'Sacramento Requisito (o relacionado)'
        }

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['nombre_periodo', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre_periodo': forms.TextInput(attrs={'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
        }
