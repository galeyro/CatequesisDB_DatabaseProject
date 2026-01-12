from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from datetime import date
from .models import Alumno, Representante, RepresentanteAlumno, Grupo, Inscripcion, Nivel, Periodo, Parroquia, Sacramento
from .forms import AlumnoForm, RepresentanteForm, GrupoForm, InscripcionForm, ParroquiaForm, NivelForm, PeriodoForm

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

    # Obtener inscripciones
    inscripciones = Inscripcion.objects.filter(id_alumno=alumno).select_related('id_grupo', 'id_grupo__id_nivel')
    
    return render(request, 'alumno_detail.html', {'alumno': alumno, 'representantes': representantes, 'inscripciones': inscripciones})

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

@login_required
def grupo_list(request):
    grupos = Grupo.objects.all().select_related('id_parroquia', 'id_nivel', 'id_periodo')
    # Anotación manual o simple loop para contar inscritos si es necesario, 
    # pero para MVP mostramos lista simple.
    return render(request, 'grupo_list.html', {'grupos': grupos})

@login_required
def grupo_create(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save()
            messages.success(request, f'Grupo creado correctamente: {grupo.id_nivel} - {grupo.id_periodo}')
            return redirect('grupo_list')
        else:
            messages.error(request, 'Error al crear el grupo. Revisa el formulario.')
    else:
        form = GrupoForm()
    
    return render(request, 'grupo_form.html', {'form': form})

@login_required
def inscripcion_create(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.id_alumno = alumno
            # Validar duplicados en el mismo grupo/periodo podría ir aquí
            try:
                inscripcion.save()
                messages.success(request, f'{alumno.nombre} inscrito correctamente.')
                return redirect('alumno_detail', pk=alumno.pk)
            except Exception as e:
                messages.error(request, f'Error al inscribir: {e}')
    else:
        # Pre-seleccionar fecha de hoy
        form = InscripcionForm(initial={'fecha_inscripcion': date.today()})


@login_required
def catalogos_home(request):
    return render(request, 'catalogos/catalogos_home.html')

# --- Parroquias ---
@login_required
def parroquia_list(request):
    parroquias = Parroquia.objects.all()
    return render(request, 'catalogos/parroquia_list.html', {'parroquias': parroquias})

@login_required
def parroquia_create(request):
    if request.method == 'POST':
        form = ParroquiaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parroquia creada correctamente.')
            return redirect('parroquia_list')
    else:
        form = ParroquiaForm()
    return render(request, 'catalogos/parroquia_form.html', {'form': form})

@login_required
def parroquia_edit(request, pk):
    parroquia = get_object_or_404(Parroquia, pk=pk)
    if request.method == 'POST':
        form = ParroquiaForm(request.POST, instance=parroquia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parroquia actualizada correctamente.')
            return redirect('parroquia_list')
    else:
        form = ParroquiaForm(instance=parroquia)
    return render(request, 'catalogos/parroquia_form.html', {'form': form, 'editing': True})

@login_required
def parroquia_delete(request, pk):
    parroquia = get_object_or_404(Parroquia, pk=pk)
    if request.method == 'POST':
        try:
            parroquia.delete()
            messages.success(request, 'Parroquia eliminada.')
            return redirect('parroquia_list')
        except Exception as e:
            messages.error(request, f'No se puede eliminar la parroquia: {e}')
    return render(request, 'catalogos/parroquia_confirm_delete.html', {'parroquia': parroquia})

# --- Niveles ---
@login_required
def nivel_list(request):
    niveles = Nivel.objects.all().order_by('orden')
    return render(request, 'catalogos/nivel_list.html', {'niveles': niveles})

@login_required
def nivel_create(request):
    if request.method == 'POST':
        form = NivelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nivel creado correctamente.')
            return redirect('nivel_list')
    else:
        form = NivelForm()
    return render(request, 'catalogos/nivel_form.html', {'form': form})

@login_required
def nivel_edit(request, pk):
    nivel = get_object_or_404(Nivel, pk=pk)
    if request.method == 'POST':
        form = NivelForm(request.POST, instance=nivel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nivel actualizado correctamente.')
            return redirect('nivel_list')
    else:
        form = NivelForm(instance=nivel)
    return render(request, 'catalogos/nivel_form.html', {'form': form, 'editing': True})

@login_required
def nivel_delete(request, pk):
    nivel = get_object_or_404(Nivel, pk=pk)
    if request.method == 'POST':
        try:
            nivel.delete()
            messages.success(request, 'Nivel eliminado.')
            return redirect('nivel_list')
        except Exception as e:
            messages.error(request, f'No se puede eliminar el nivel: {e}')
    return render(request, 'catalogos/nivel_confirm_delete.html', {'nivel': nivel})

# --- Periodos ---
@login_required
def periodo_list(request):
    periodos = Periodo.objects.all().order_by('-fecha_inicio')
    return render(request, 'catalogos/periodo_list.html', {'periodos': periodos})

@login_required
def periodo_create(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Periodo creado correctamente.')
            return redirect('periodo_list')
    else:
        form = PeriodoForm()
    return render(request, 'catalogos/periodo_form.html', {'form': form})

@login_required
def periodo_edit(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    if request.method == 'POST':
        form = PeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Periodo actualizado correctamente.')
            return redirect('periodo_list')
    else:
        form = PeriodoForm(instance=periodo)
    return render(request, 'catalogos/periodo_form.html', {'form': form, 'editing': True})

@login_required
def periodo_delete(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    if request.method == 'POST':
        try:
            periodo.delete()
            messages.success(request, 'Periodo eliminado.')
            return redirect('periodo_list')
        except Exception as e:
            messages.error(request, f'No se puede eliminar el periodo: {e}')
    return render(request, 'catalogos/periodo_confirm_delete.html', {'periodo': periodo})
