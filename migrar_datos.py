import csv
import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
django.setup()

from gestor_documentos.models import Asegurado
from django.contrib.auth.models import User

def migrar_datos(csv_file):
    # Obtener el primer usuario (o crear uno si no existe)
    try:
        usuario = User.objects.first()
    except:
        usuario = User.objects.create_user('admin', 'admin@example.com', 'admin')
        usuario.is_staff = True
        usuario.save()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Convertir fecha si existe
                fecha_nacimiento = None
                if row.get('fecha_nacimiento'):
                    try:
                        fecha_nacimiento = datetime.strptime(row['fecha_nacimiento'], '%Y-%m-%d').date()
                    except:
                        pass

                # Crear el asegurado
                asegurado = Asegurado.objects.create(
                    id_asegurado=row.get('id_asegurado'),
                    id_poliza=row.get('id_poliza'),
                    nombre=row.get('nombre'),
                    apellido_paterno=row.get('apellido_paterno'),
                    apellido_materno=row.get('apellido_materno'),
                    fecha_nacimiento=fecha_nacimiento,
                    genero=row.get('genero', 'O'),
                    rfc=row.get('rfc'),
                    email=row.get('email'),
                    telefono=row.get('telefono'),
                    titulat_conyuge_dependiente=row.get('titulat_conyuge_dependiente'),
                    iniciar_reclamo=row.get('iniciar_reclamo', '').lower() == 'true',
                    diagnostico=row.get('diagnostico'),
                    numero_factura1=row.get('numero_factura1'),
                    importe_factura1=row.get('importe_factura1'),
                    dia1=row.get('dia1'),
                    dia2=row.get('dia2'),
                    mes1=row.get('mes1'),
                    mes2=row.get('mes2'),
                    año1=row.get('año1'),
                    año2=row.get('año2'),
                    año3=row.get('año3'),
                    año4=row.get('año4'),
                    usuario=usuario
                )
                print(f"Asegurado creado: {asegurado.nombre} {asegurado.apellido_paterno}")
            except Exception as e:
                print(f"Error al crear asegurado: {str(e)}")

if __name__ == '__main__':
    # Reemplaza 'datos_asegurados.csv' con el nombre de tu archivo CSV
    migrar_datos('datos_asegurados.csv') 