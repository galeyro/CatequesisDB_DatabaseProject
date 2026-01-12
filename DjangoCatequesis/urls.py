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
]
