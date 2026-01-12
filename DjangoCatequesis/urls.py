from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),
    
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sql/', views.sql_home, name='sql_home'),
    
    # SQL Views
    path('alumnos/', views.alumno_list, name='alumno_list'),
    path('alumnos/nuevo/', views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/', views.alumno_detail, name='alumno_detail'),
    path('alumnos/<int:pk>/editar/', views.alumno_edit, name='alumno_edit'),
    path('alumnos/<int:pk>/borrar/', views.alumno_delete, name='alumno_delete'),
    
    # Grupos e Inscripciones
    path('grupos/', views.grupo_list, name='grupo_list'),
    path('grupos/nuevo/', views.grupo_create, name='grupo_create'),
    path('alumnos/<int:alumno_id>/inscribir/', views.inscripcion_create, name='inscripcion_create'),
    
    # Catalogos
    path('catalogos/', views.catalogos_home, name='catalogos_home'),
    
    # Parroquias
    path('catalogos/parroquias/', views.parroquia_list, name='parroquia_list'),
    path('catalogos/parroquias/nueva/', views.parroquia_create, name='parroquia_create'),
    path('catalogos/parroquias/<int:pk>/editar/', views.parroquia_edit, name='parroquia_edit'),
    path('catalogos/parroquias/<int:pk>/borrar/', views.parroquia_delete, name='parroquia_delete'),

    # Niveles
    path('catalogos/niveles/', views.nivel_list, name='nivel_list'),
    path('catalogos/niveles/nuevo/', views.nivel_create, name='nivel_create'),
    path('catalogos/niveles/<int:pk>/editar/', views.nivel_edit, name='nivel_edit'),
    path('catalogos/niveles/<int:pk>/borrar/', views.nivel_delete, name='nivel_delete'),

    # Periodos
    path('catalogos/periodos/', views.periodo_list, name='periodo_list'),
    path('catalogos/periodos/nuevo/', views.periodo_create, name='periodo_create'),
    path('catalogos/periodos/<int:pk>/editar/', views.periodo_edit, name='periodo_edit'),
    path('catalogos/periodos/<int:pk>/borrar/', views.periodo_delete, name='periodo_delete'),
]
