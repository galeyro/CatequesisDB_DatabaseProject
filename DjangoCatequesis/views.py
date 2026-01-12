from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Alumno, Representante, RepresentanteAlumno
from .forms import AlumnoForm, RepresentanteForm

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def sql_home(request):
    # Redirigir por defecto a la lista de alumnos
    return redirect('alumno_list')

@login_required
def alumno_list(request):
    query = request.GET.get('q', '')
    if query:
        alumnos = Alumno.objects.filter(nombre__icontains=query) | Alumno.objects.filter(apellido__icontains=query)
    else:
        alumnos = Alumno.objects.all().order_by('apellido', 'nombre')
    
    context = {
        'alumnos': alumnos,
        'query': query
    }
    return render(request, 'alumno_list.html', context)

@login_required
@transaction.atomic
def alumno_create(request):
    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST, prefix='alumno')
        representante_form = RepresentanteForm(request.POST, prefix='representante')
        
        if alumno_form.is_valid() and representante_form.is_valid():
            # 1. Guardar Alumno
            alumno = alumno_form.save()
            
            # 2. Guardar Representante
            representante = representante_form.save()
            
            # 3. Crear relación M:N
            RepresentanteAlumno.objects.create(
                alumno_id_alumno=alumno,
                representante_id_representante=representante
            )
            
            messages.success(request, f'Alumno {alumno.nombre} registrado correctamente con su representante.')
            return redirect('alumno_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        alumno_form = AlumnoForm(prefix='alumno')
        representante_form = RepresentanteForm(prefix='representante')

    context = {
        'alumno_form': alumno_form,
        'representante_form': representante_form
    }
    return render(request, 'alumno_form.html', context)

@login_required
def alumno_detail(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    # Obtener representantes relación manual
    relaciones = RepresentanteAlumno.objects.filter(alumno_id_alumno=alumno)
    representantes = [rel.representante_id_representante for rel in relaciones]
    
    return render(request, 'alumno_detail.html', {'alumno': alumno, 'representantes': representantes})

@login_required
@transaction.atomic
def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    
    # Intentar obtener el primer representante vinculado (lógica simplificada para este MVP)
    # En un futuro se podría manejar una lista de representantes para editar
    relacion = RepresentanteAlumno.objects.filter(alumno_id_alumno=alumno).first()
    representante = relacion.representante_id_representante if relacion else None

    if request.method == 'POST':
        alumno_form = AlumnoForm(request.POST, instance=alumno, prefix='alumno')
        representante_form = RepresentanteForm(request.POST, instance=representante, prefix='representante')
        
        if alumno_form.is_valid() and representante_form.is_valid():
            try:
                alumno_saved = alumno_form.save()
                rep_saved = representante_form.save()
                
                # Si no existía relación, la creamos ahora (caso borde)
                if not relacion:
                    RepresentanteAlumno.objects.create(
                        alumno_id_alumno=alumno_saved,
                        representante_id_representante=rep_saved
                    )
                
                messages.success(request, f'Datos de {alumno.nombre} actualizados correctamente.')
                return redirect('alumno_detail', pk=alumno.pk)
            except Exception as e:
                messages.error(request, f'Error al guardar los cambios: {e}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        alumno_form = AlumnoForm(instance=alumno, prefix='alumno')
        representante_form = RepresentanteForm(instance=representante, prefix='representante')
    
    context = {
        'alumno_form': alumno_form,
        'representante_form': representante_form,
        'editing': True,
        'alumno': alumno
    }
    return render(request, 'alumno_form.html', context)

@login_required
def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    
    if request.method == 'POST':
        try:
            nombre = f"{alumno.nombre} {alumno.apellido}"
            alumno.delete()
            messages.success(request, f'El alumno {nombre} ha sido eliminado correctamente.')
            return redirect('alumno_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el alumno: {e}')
            return redirect('alumno_detail', pk=pk)
            
    return render(request, 'alumno_confirm_delete.html', {'alumno': alumno})