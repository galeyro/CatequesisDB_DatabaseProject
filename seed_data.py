
import os
import django
import sys
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCatequesis.settings')
django.setup()

from DjangoCatequesis.models import Nivel, Periodo, Parroquia, Sacramento

def seed():
    print("Iniciando carga de datos...")
    
    # 1. Crear Sacramentos
    try:
        s1, _ = Sacramento.objects.get_or_create(nombre_sacramento='Bautismo')
        s2, _ = Sacramento.objects.get_or_create(nombre_sacramento='Primera Comunión')
        s3, _ = Sacramento.objects.get_or_create(nombre_sacramento='Confirmación')
        print("Sacramentos creados/verificados.")
    except Exception as e:
        print(f"Error creando Sacramentos: {e}")

    # 2. Crear Niveles
    niveles = [
        ('Nivel 1 (Iniciación)', 1, s2),
        ('Nivel 2 (Reconciliación)', 2, s2),
        ('Nivel 3 (Eucaristía)', 3, s2),
        ('Año Bíblico - Pre-Confirmación', 4, s3),
        ('Confirmación 1', 5, s3),
        ('Confirmación 2', 6, s3),
    ]
    
    for nombre, orden, sacr in niveles:
        try:
            Nivel.objects.get_or_create(nombre_nivel=nombre, orden=orden, sacramento_id_sacramento=sacr)
        except Exception as e:
            print(f"Error creando Nivel {nombre}: {e}")
    print("Niveles procesados.")

    # 3. Crear Periodo
    try:
        Periodo.objects.get_or_create(
            nombre_periodo='2025-2026', 
            defaults={'fecha_inicio': date(2025, 9, 1), 'fecha_fin': date(2026, 6, 30)}
        )
        print("Periodo creado/verificado.")
    except Exception as e:
        print(f"Error creando Periodo: {e}")

    # 4. Crear Parroquia
    try:
        Parroquia.objects.get_or_create(nombre_parroquia='Parroquia San Francisco', defaults={'direccion': 'Centro'})
        print("Parroquia creada/verificada.")
    except Exception as e:
        print(f"Error creando Parroquia: {e}")

if __name__ == '__main__':
    seed()
