from django.contrib import admin
from .models import (
    Alumno, Catequista, Documento, Grupo, GrupoCatequista, Inscripcion,
    InscripcionPadrino, Nivel, Padrino, Parroquia, Perfil, Periodo,
    Representante, RepresentanteAlumno, Sacramento, SacramentoRealizado, Usuario
)

admin.site.register(Alumno)
admin.site.register(Catequista)
admin.site.register(Documento)
admin.site.register(Grupo)
admin.site.register(GrupoCatequista)
admin.site.register(Inscripcion)
admin.site.register(InscripcionPadrino)
admin.site.register(Nivel)
admin.site.register(Padrino)
admin.site.register(Parroquia)
admin.site.register(Perfil)
admin.site.register(Periodo)
admin.site.register(Representante)
admin.site.register(RepresentanteAlumno)
admin.site.register(Sacramento)
admin.site.register(SacramentoRealizado)
admin.site.register(Usuario)
