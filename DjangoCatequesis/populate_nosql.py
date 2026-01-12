import pymongo
from bson import ObjectId
from datetime import datetime
import random

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Conexión
uri = os.getenv('MONGO_URI')
print(f"Conectando a: {uri}")

client = pymongo.MongoClient(
    uri,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000
)
db = client['CatequesisDB']

# Limpiar colecciones
db.catequistas.delete_many({})
db.alumnos.delete_many({})
db.grupos.delete_many({})

print("Base de datos limpia.")

# --- CATEQUISTAS ---
catequistas_data = [
    {
        'username': 'marta.perez@email.com',
        'rol': 'catequista',
        'datosPersonales': {
            'nombre': 'Marta',
            'apellido': 'Perez',
            'fechaNacimiento': datetime(1985, 5, 20),
            'email': 'marta.perez@email.com',
            'telefono': '099111222',
            'direccion': 'Calle A 123'
        }
    },
    {
        'username': 'juan.lopez@email.com',
        'rol': 'coordinador',
        'datosPersonales': {
            'nombre': 'Juan',
            'apellido': 'Lopez',
            'fechaNacimiento': datetime(1980, 8, 15),
            'email': 'juan.lopez@email.com',
            'telefono': '099333444',
            'direccion': 'Av. Principal 456'
        }
    },
    {
        'username': 'ana.garcia@email.com',
        'rol': 'catequista',
        'datosPersonales': {
            'nombre': 'Ana',
            'apellido': 'Garcia',
            'fechaNacimiento': datetime(1990, 2, 10),
            'email': 'ana.garcia@email.com',
            'telefono': '099555666',
            'direccion': 'Plaza Central 789'
        }
    }
]

catequistas_ids = db.catequistas.insert_many(catequistas_data).inserted_ids
print(f"Insertados {len(catequistas_ids)} catequistas.")

# --- ALUMNOS ---
alumnos_ids = []
for i in range(15):
    nombre = f"Alumno{i+1}"
    apellido = f"Apellido{i+1}"
    
    alumno = {
        'idSql': None,
        'datosPersonales': {
            'nombre': nombre,
            'apellido': apellido,
            'fechaNacimiento': datetime(2010 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
            'lugarNacimiento': 'Ciudad Ejemplo',
            'direccion': f'Calle {random.randint(1,100)}',
            'telefono': f'098{random.randint(100000, 999999)}',
            'infoEscolar': 'Escuela Primaria Local',
            'infoSalud': 'Ninguna' if random.random() > 0.2 else 'Alergia al polvo'
        },
        'representantes': [
            {
                'nombre': f'RepNombre{i+1}',
                'apellido': f'RepApellido{i+1}',
                'ocupacion': 'Empleado',
                'telefono': f'099{random.randint(100000, 999999)}',
                'email': f'rep{i+1}@email.com'
            }
        ],
        'historialSacramentos': [],
        'esInscripcionActiva': True
    }
    
    # Algunos con bautismo
    if random.random() > 0.5:
        alumno['historialSacramentos'].append({
            'nombreSacramento': 'Bautismo',
            'fechaRealizacion': datetime(2011 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
            'lugar': 'Parroquia San Jose',
            'documentos': {
                'id': f'DOC-{random.randint(1000, 9999)}',
                'emitidoPor': 'Parroquia San Jose',
                'fecha': datetime.now()
            }
        })

    res = db.alumnos.insert_one(alumno)
    alumnos_ids.append(res.inserted_id)

print(f"Insertados {len(alumnos_ids)} alumnos.")

# --- GRUPOS ---
niveles = ['Primera Comunión 1', 'Primera Comunión 2', 'Confirmación 1', 'Confirmación 2']

for j in range(3):
    nivel = random.choice(niveles)
    
    # Asignar 1 o 2 catequistas aleatorios
    cats_asignados = random.sample(list(catequistas_ids), k=random.randint(1, 2))
    catequistas_embedded = []
    for cid in cats_asignados:
        c_doc = db.catequistas.find_one({'_id': cid})
        nombre_completo = f"{c_doc['datosPersonales']['nombre']} {c_doc['datosPersonales']['apellido']}"
        catequistas_embedded.append({
            'id': str(cid),
            'nombreCompleto': nombre_completo
        })

    # Asignar 3-5 alumnos aleatorios
    alumnos_asignados = random.sample(alumnos_ids, k=random.randint(3, 5))
    alumnos_embedded = []
    
    for aid in alumnos_asignados:
        a_doc = db.alumnos.find_one({'_id': aid})
        nombre_completo = f"{a_doc['datosPersonales']['nombre']} {a_doc['datosPersonales']['apellido']}"
        
        embedded_data = {
            'idAlumno': aid, # ObjectId real
            'nombreCompleto': nombre_completo,
            'estadoInscripcion': 'Confirmado' if random.random() > 0.2 else 'Pendiente'
        }
        
        # 50% chance de tener padrino
        if random.random() > 0.5:
            embedded_data['padrino'] = {
                'nombre': f'Padrino{j}-{random.randint(1,10)}',
                'apellido': 'PadrinoApellido',
                'telefono': '091234567'
            }
            
        alumnos_embedded.append(embedded_data)

    grupo = {
        'datosGenerales': {
            'nombreGrupo': f'Grupo {nivel} - {chr(65+j)}',
            'nivel': {'id': j+1, 'nombre': nivel},
            'periodo': {'id': 1, 'nombre': '2025-2026'}
        },
        'catequistas': catequistas_embedded,
        'alumnosInscritos': alumnos_embedded
    }
    
    db.grupos.insert_one(grupo)

print("Insertados 3 grupos con relaciones.")
print("Script finalizado exitosamente.")
