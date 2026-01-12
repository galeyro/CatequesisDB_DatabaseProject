from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponseBadRequest
from .utils_mongo import get_db
from bson.objectid import ObjectId
from bson.objectid import ObjectId
from datetime import datetime
import json
from bson import json_util

def nosql_home(request):
    return render(request, 'nosql/home.html', {'is_nosql': True})

# --- HELPER GENERICO (Simplificado) ---
def parse_multi_level_post(request):
    """
    Parsea campos anidados tipo 'datos.nombre' y arrays 'lista[0].campo'
    """
    data_out = {}
    
    # Logic similar a process_alumno_form pero mas generico si fuera necesario
    # Por ahora mantenemos el especifico, y agregamos uno de Grupos
    return data_out

# --- ALUMNOS ---

def alumno_list(request):
    db = get_db()
    alumnos = list(db.alumnos.find())
    # Convertir ObjectId a string para el template
    for a in alumnos:
        a['id'] = str(a['_id'])
    return render(request, 'nosql/alumno_list.html', {'alumnos': alumnos, 'is_nosql': True})

# --- HELPER PARA PROCESAR FORMULARIO COMPLEJO ---
def process_alumno_form(request):
    """
    Parsea el request.POST para reconstruir arrays dinámicos (representantes, sacramentos)
    y objetos anidados (datosPersonales).
    """
    # 1. Datos Personales (Simple)
    fecha_nacimiento_str = request.POST.get('fechaNacimiento')
    fecha_nacimiento = None
    if fecha_nacimiento_str:
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d')
        except ValueError:
            pass

    data = {
        'datosPersonales': {
            'nombre': request.POST.get('nombre'),
            'apellido': request.POST.get('apellido'),
            'fechaNacimiento': fecha_nacimiento,
            'lugarNacimiento': request.POST.get('lugarNacimiento'),
            'direccion': request.POST.get('direccion'),
            'telefono': request.POST.get('telefono'),
            'infoEscolar': request.POST.get('infoEscolar'),
            'infoSalud': request.POST.get('infoSalud'),
        },
        # 'esInscripcionActiva': True, # Se manejará en el create o si viene en el POST
        'representantes': [],
        'historialSacramentos': []
    }

    # 2. Procesar Arrays Dinámicos (búsqueda por patrones en claves POST)
    # Patrones esperados: "representantes[0].nombre", "sacramentos[0].documentos.id"
    
    # --- REPRESENTANTES ---
    reps_map = {} # indice -> objeto
    for key, value in request.POST.items():
        if key.startswith('representantes['):
            # Ejemplo: representantes[0].nombre
            try:
                # Extraer indice y campo
                parts = key.split('.')
                main_part = parts[0] # representantes[0]
                field_name = parts[1] # nombre
                
                idx_str = main_part.replace('representantes[', '').replace(']', '')
                idx = int(idx_str)
                
                if idx not in reps_map:
                    reps_map[idx] = {}
                
                reps_map[idx][field_name] = value
            except:
                continue
    
    # Convertir mapa a lista ordenada
    for idx in sorted(reps_map.keys()):
        data['representantes'].append(reps_map[idx])

    # --- SACRAMENTOS ---
    sacs_map = {}
    for key, value in request.POST.items():
        if key.startswith('sacramentos['):
            # Ejemplo: sacramentos[0].nombreSacramento o sacramentos[0].documentos.id
            try:
                parts = key.split('.')
                main_part = parts[0] # sacramentos[0]
                
                idx_str = main_part.replace('sacramentos[', '').replace(']', '')
                idx = int(idx_str)
                
                if idx not in sacs_map:
                    sacs_map[idx] = {'documentos': {}}
                
                if parts[1] == 'documentos':
                    # Es un subcampo de documentos (ej: id, emitidoPor)
                    doc_field = parts[2]
                    
                    # Convertir fecha documento si aplica
                    if doc_field == 'fecha' and value:
                         try:
                            value = datetime.strptime(value, '%Y-%m-%d')
                         except:
                            pass
                    
                    sacs_map[idx]['documentos'][doc_field] = value
                else:
                    field_name = parts[1]
                    # Convertir fecha realizacion
                    if field_name == 'fechaRealizacion' and value:
                         try:
                            value = datetime.strptime(value, '%Y-%m-%d')
                         except:
                            pass
                    
                    sacs_map[idx][field_name] = value
            except Exception as e:
                print(f"Error parseando key {key}: {e}")
                continue

    for idx in sorted(sacs_map.keys()):
        data['historialSacramentos'].append(sacs_map[idx])
        
    return data

def alumno_create(request):
    if request.method == 'POST':
        db = get_db()
        data = process_alumno_form(request)
        
        # Valores por defecto para creación
        data['esInscripcionActiva'] = True
        
        # Asignar ID SQL manual si fuera necesario (simulado)
        # data['idSql'] = 999 
        
        db.alumnos.insert_one(data)
        return redirect('nosql_alumno_list')
    
    # Contexto inicial vacío para JS
    context = {
        'alumno': {},
        'is_nosql': True,
        'representantes_json': '[]',
        'sacramentos_json': '[]'
    }
    return render(request, 'nosql/alumno_form.html', context)

def alumno_edit(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        raise Http404("ID invalido")

    alumno = db.alumnos.find_one({'_id': obj_id})
    if not alumno:
        raise Http404("Alumno no encontrado")
        
    if request.method == 'POST':
        update_data = process_alumno_form(request)
        db.alumnos.update_one({'_id': obj_id}, {'$set': update_data})
        return redirect('nosql_alumno_list')
        
    alumno['id'] = str(alumno['_id'])
    
    # Pre-procesar fecha nacimiento principal
    if alumno.get('datosPersonales', {}).get('fechaNacimiento'):
        fecha = alumno['datosPersonales']['fechaNacimiento']
        if isinstance(fecha, datetime):
            alumno['fechaNacimiento_fmt'] = fecha.strftime('%Y-%m-%d')
            
    # Serializar arrays para JS (usando default de json_util para fechas/ObjetoId si hubieran)
    representantes_list = alumno.get('representantes', [])
    sacramentos_list = alumno.get('historialSacramentos', [])
    
    # Helper simple para JSON
    def json_serial(obj):
        if isinstance(obj, (datetime)):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return str(obj)

    context = {
        'alumno': alumno,
        'is_nosql': True,
        'representantes_json': json.dumps(representantes_list, default=json_serial),
        'sacramentos_json': json.dumps(sacramentos_list, default=json_serial)
    }
    
    return render(request, 'nosql/alumno_form.html', context)

def alumno_detail(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        raise Http404("ID invalido")
    
    alumno = db.alumnos.find_one({'_id': obj_id})
    if not alumno:
        raise Http404("Alumno no encontrado")
    
    alumno['id'] = str(alumno['_id'])
    
    # Formatear fechas si existen para visualización
    # (Opcional si se usa el filtro |date en template, pero útil para depurar)
    
    return render(request, 'nosql/alumno_detail.html', {'alumno': alumno, 'is_nosql': True})

def alumno_delete(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        return redirect('nosql_alumno_list')
        
    db.alumnos.delete_one({'_id': obj_id})
    return redirect('nosql_alumno_list')

# --- GRUPOS ---

def grupo_list(request):
    db = get_db()
    grupos = list(db.grupos.find())
    for g in grupos:
        g['id'] = str(g['_id'])
    return render(request, 'nosql/grupo_list.html', {'grupos': grupos, 'is_nosql': True})

def grupo_create(request):
    db = get_db()
    if request.method == 'POST':
        
        # Procesar catequistas
        # Procesar catequistas (Look up names by ID)
        catequistas = []
        for key, value in request.POST.items():
            if key.startswith('catequistas[') and 'id' in key:
                if value.strip():
                    # value is the ID. We find the name in DB or from hidden field?
                    # Better from DB to be safe, or just trust the select text?
                    # The select sends value (ID). We need the text.
                    # Simplified: We will lookup.
                    try:
                        cat_obj = db.catequistas.find_one({'_id': ObjectId(value)})
                        if cat_obj:
                            nombre = f"{cat_obj.get('datosPersonales', {}).get('nombre', '')} {cat_obj.get('datosPersonales', {}).get('apellido', '')}".strip()
                            catequistas.append({'id': value, 'nombreCompleto': nombre})
                    except:
                        pass
        
        data = {
            'datosGenerales': {
                'nombreGrupo': request.POST.get('nombreGrupo'),
                'nivel': {'nombre': request.POST.get('nivel')},
                'periodo': {'nombre': request.POST.get('periodo')},
            },
            'catequistas': catequistas,
            'alumnosInscritos': [] # Array simple de IDs o objetos minimos
        }
        
        db.grupos.insert_one(data)
        return redirect('nosql_grupo_list')

    # Fetch all catequistas for the dropdown
    all_catequistas = list(db.catequistas.find({}, {'_id': 1, 'datosPersonales.nombre': 1, 'datosPersonales.apellido': 1}))
    # Helper to format for JS
    catequistas_opts = []
    for c in all_catequistas:
        nombre = f"{c.get('datosPersonales', {}).get('nombre', '')} {c.get('datosPersonales', {}).get('apellido', '')}".strip()
        catequistas_opts.append({'id': str(c['_id']), 'nombreCompleto': nombre})

    return render(request, 'nosql/grupo_form.html', {
        'is_nosql': True, 
        'catequistas_json': '[]',
        'available_catequistas_json': json.dumps(catequistas_opts)
    })

def grupo_edit(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        raise Http404("ID Invalido")
        
    grupo = db.grupos.find_one({'_id': obj_id})
    if not grupo:
        raise Http404("Grupo no encontrado")

    if request.method == 'POST':
         # Procesar catequistas again (Don't Repeat Yourself: refactor later if needed)
        # Procesar catequistas again
        catequistas = []
        for key, value in request.POST.items():
            if key.startswith('catequistas[') and 'id' in key:
                 if value.strip():
                    try:
                        cat_obj = db.catequistas.find_one({'_id': ObjectId(value)})
                        if cat_obj:
                            nombre = f"{cat_obj.get('datosPersonales', {}).get('nombre', '')} {cat_obj.get('datosPersonales', {}).get('apellido', '')}".strip()
                            catequistas.append({'id': value, 'nombreCompleto': nombre})
                    except:
                        pass
        
        update_data = {
            'datosGenerales.nombreGrupo': request.POST.get('nombreGrupo'),
            'datosGenerales.nivel.nombre': request.POST.get('nivel'),
            'datosGenerales.periodo.nombre': request.POST.get('periodo'),
            'catequistas': catequistas
        }
        
        db.grupos.update_one({'_id': obj_id}, {'$set': update_data})
        return redirect('nosql_grupo_list')
        
    grupo['id'] = str(grupo['_id'])

    # Fetch all catequistas for the dropdown
    all_catequistas = list(db.catequistas.find({}, {'_id': 1, 'datosPersonales.nombre': 1, 'datosPersonales.apellido': 1}))
    catequistas_opts = []
    for c in all_catequistas:
        nombre = f"{c.get('datosPersonales', {}).get('nombre', '')} {c.get('datosPersonales', {}).get('apellido', '')}".strip()
        catequistas_opts.append({'id': str(c['_id']), 'nombreCompleto': nombre})

    return render(request, 'nosql/grupo_form.html', {
        'grupo': grupo, 
        'is_nosql': True,
        'catequistas_json': json.dumps(grupo.get('catequistas', [])),
        'available_catequistas_json': json.dumps(catequistas_opts)
    })

def grupo_delete(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        pass
    db.grupos.delete_one({'_id': obj_id})
    db.grupos.delete_one({'_id': obj_id})
    return redirect('nosql_grupo_list')

def grupo_detail(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        raise Http404("ID invalido")
        
    grupo = db.grupos.find_one({'_id': obj_id})
    if not grupo:
        raise Http404("Grupo no encontrado")

    grupo['id'] = str(grupo['_id'])
    
    # Podriamos enriquecer alumnosInscritos aqui si son solo IDs, pero por ahora lo dejamos raw
    
    return render(request, 'nosql/grupo_detail.html', {'grupo': grupo, 'is_nosql': True})

# --- CATEQUISTAS ---

def catequista_list(request):
    db = get_db()
    catequistas = list(db.catequistas.find())
    for c in catequistas:
        c['id'] = str(c['_id'])
    return render(request, 'nosql/catequista_list.html', {'catequistas': catequistas, 'is_nosql': True})

def catequista_create(request):
    if request.method == 'POST':
        db = get_db()
        data = {
            'username': request.POST.get('email'), # Usamos email como username por defecto
            'rol': 'catequista',
            'datosPersonales': {
                'nombre': request.POST.get('nombre'),
                'apellido': request.POST.get('apellido'),
                'fechaNacimiento': request.POST.get('fechaNacimiento'), # fecha nacimiento string
                'email': request.POST.get('email'),
                'telefono': request.POST.get('telefono'),
                'direccion': request.POST.get('direccion'),
            }
        }
        # Parse fecha nacimiento if exists
        dob = data['datosPersonales']['fechaNacimiento']
        if dob:
            try:
                data['datosPersonales']['fechaNacimiento'] = datetime.strptime(dob, '%Y-%m-%d')
            except:
                pass

        db.catequistas.insert_one(data)
        return redirect('nosql_catequista_list')

    return render(request, 'nosql/catequista_form.html', {'is_nosql': True})

def catequista_edit(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        raise Http404("ID invalido")
    
    cat = db.catequistas.find_one({'_id': obj_id})
    if not cat:
        raise Http404("Catequista no encontrado")

    if request.method == 'POST':
        update_data = {
            'datosPersonales.nombre': request.POST.get('nombre'),
            'datosPersonales.apellido': request.POST.get('apellido'),
            'datosPersonales.email': request.POST.get('email'),
            'datosPersonales.telefono': request.POST.get('telefono'),
            'datosPersonales.direccion': request.POST.get('direccion'),
        }
        
        dob = request.POST.get('fechaNacimiento')
        if dob:
             try:
                update_data['datosPersonales.fechaNacimiento'] = datetime.strptime(dob, '%Y-%m-%d')
             except:
                pass

        db.catequistas.update_one({'_id': obj_id}, {'$set': update_data})
        return redirect('nosql_catequista_list')

    cat['id'] = str(cat['_id'])
    
    # Format date for input
    if cat.get('datosPersonales', {}).get('fechaNacimiento'):
        f = cat['datosPersonales']['fechaNacimiento']
        if isinstance(f, datetime):
            cat['fechaNacimiento_fmt'] = f.strftime('%Y-%m-%d')

    return render(request, 'nosql/catequista_form.html', {'catequista': cat, 'is_nosql': True})

def catequista_delete(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        pass
    db.catequistas.delete_one({'_id': obj_id})
    return redirect('nosql_catequista_list')

def catequista_detail(request, id):
    db = get_db()
    try:
        obj_id = ObjectId(id)
    except:
        raise Http404("ID invalido")
    
    cat = db.catequistas.find_one({'_id': obj_id})
    if not cat:
        raise Http404("Catequista no encontrado")
    
    cat['id'] = str(cat['_id'])
    return render(request, 'nosql/catequista_detail.html', {'catequista': cat, 'is_nosql': True})
