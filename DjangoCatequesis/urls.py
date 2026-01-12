from django.contrib import admin
from django.urls import path, include
from . import views
from . import views_nosql

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),
    
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sql/', views.sql_home, name='sql_home'),
    
    # NoSQL Views
    path('nosql/', views_nosql.nosql_home, name='nosql_home'),
    path('nosql/alumnos/', views_nosql.alumno_list, name='nosql_alumno_list'),
    path('nosql/alumnos/nuevo/', views_nosql.alumno_create, name='nosql_alumno_create'),
    path('nosql/alumnos/<str:id>/editar/', views_nosql.alumno_edit, name='nosql_alumno_edit'),
    path('nosql/alumnos/<str:id>/', views_nosql.alumno_detail, name='nosql_alumno_detail'),
    path('nosql/alumnos/<str:id>/borrar/', views_nosql.alumno_delete, name='nosql_alumno_delete'),
    
    path('nosql/grupos/', views_nosql.grupo_list, name='nosql_grupo_list'),
    path('nosql/grupos/nuevo/', views_nosql.grupo_create, name='nosql_grupo_create'),
    path('nosql/grupos/<str:id>/editar/', views_nosql.grupo_edit, name='nosql_grupo_edit'),
    path('nosql/grupos/<str:id>/', views_nosql.grupo_detail, name='nosql_grupo_detail'),
    path('nosql/grupos/<str:id>/borrar/', views_nosql.grupo_delete, name='nosql_grupo_delete'),
    path('nosql/catequistas/', views_nosql.catequista_list, name='nosql_catequista_list'),
    path('nosql/catequistas/nuevo/', views_nosql.catequista_create, name='nosql_catequista_create'),
    path('nosql/catequistas/<str:id>/editar/', views_nosql.catequista_edit, name='nosql_catequista_edit'),
    path('nosql/catequistas/<str:id>/', views_nosql.catequista_detail, name='nosql_catequista_detail'),
    path('nosql/catequistas/<str:id>/borrar/', views_nosql.catequista_delete, name='nosql_catequista_delete'),
    
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
