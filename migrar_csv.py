import os
import django
import pandas as pd
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
django.setup()

from gestion_asegurados.models import (
    Compania, AseguradoraPlan, Poliza, Asegurado,
    Diagnostico, Medico, InformeMedico, Factura, PartidaFactura
)

def limpiar_fecha(fecha_str):
    if pd.isna(fecha_str):
        return None
    try:
        if isinstance(fecha_str, str):
            return datetime.strptime(fecha_str, '%Y-%m-%d').date()
        return fecha_str.date()
    except ValueError:
        return None

def migrar_companias(csv_path):
    print("Migrando Compañías...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            Compania.objects.get_or_create(
                id_aseguradora=row['ID_Aseguradora'],
                defaults={
                    'nombre': row['Nombre'],
                    'nombre_corto': row['Nombre_Corto']
                }
            )
        except Exception as e:
            print(f"Error al migrar compañía {row['Nombre']}: {str(e)}")
    print("Migración de Compañías completada.")

def migrar_planes(csv_path):
    print("Migrando Planes...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            compania = Compania.objects.get(id_aseguradora=row['ID_Aseguradora'])
            AseguradoraPlan.objects.get_or_create(
                id_plan=row['ID_Plan'],
                defaults={
                    'id_aseguradora': compania,
                    'nombre': row['Nombre']
                }
            )
        except Exception as e:
            print(f"Error al migrar plan {row['ID_Plan']}: {str(e)}")
    print("Migración de Planes completada.")

def migrar_polizas(csv_path):
    print("Migrando Pólizas...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            compania = Compania.objects.get(id_aseguradora=row['ID_Aseguradora'])
            plan = AseguradoraPlan.objects.get(id_plan=row['ID_Plan'])
            
            Poliza.objects.get_or_create(
                id_poliza=row['ID_Poliza'],
                defaults={
                    'id_aseguradora': compania,
                    'id_plan': plan,
                    'numero_poliza': row['Numero_Poliza'],
                    'fisica_moral': row['Fisica_Moral?'],
                    'contratante_moral': row['Contratante_Moral'],
                    'folio_mercantil': row['Folio_Mercantil'],
                    'objeto_social': row['Objeto_Social'],
                    'nombre': row['Nombre'],
                    'apellido_paterno': row['Apellido_Paterno'],
                    'apellido_materno': row['Apellido_Materno'],
                    'fecha_nacimiento': limpiar_fecha(row['Fecha_Nacimiento']),
                    'lugar_nacimiento': row['Lugar_Nacimiento'],
                    'curp': row['CURP'],
                    'pais_nacimiento': row['Pais_Nacimiento'],
                    'nacionalidad': row['Nacionalidad'],
                    'rfc': row['RFC'],
                    'profesion': row['Profesion'],
                    'calle': row['Calle'],
                    'numero_exterior': row['Numero_Exterior'],
                    'numero_interior': row['Numero_Interior'],
                    'colonia': row['Colonia'],
                    'municipio_delegacion': row['Municipio_Delegacion'],
                    'entidad_federativa': row['Entidad_Federativa'],
                    'ciudad_poblacion': row['Ciudad_Poblacion'],
                    'codigo_postal': row['Codigo_Postal'],
                    'telefono': row['Telefono'],
                    'email': row['Email'],
                    'es_gobierno': row['Gobierno?'],
                    'cargo': row['Cargo'],
                    'dependencia': row['Dependencia'],
                    'actua_nombre_propio': row['Actua_Nombre_Propio?'],
                    'titular_contratante': row['Titular_Contratante'],
                    'clabe': row['Clabe'],
                    'banco': row['Banco'],
                    'observaciones': row['Observaciones']
                }
            )
        except Exception as e:
            print(f"Error al migrar póliza {row['ID_Poliza']}: {str(e)}")
    print("Migración de Pólizas completada.")

def migrar_diagnosticos(csv_path):
    print("Migrando Diagnósticos...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            asegurado = Asegurado.objects.get(id_asegurado=row['ID_Asegurado'])
            Diagnostico.objects.get_or_create(
                id_diagnostico=row['ID_Diagnostico'],
                defaults={
                    'id_asegurado': asegurado,
                    'nombre': row['Nombre'],
                    'diagnostico': row['Diagnostico'],
                    'fecha_inicio_padecimiento': limpiar_fecha(row['Fecha_Inicio_Padecimiento']),
                    'fecha_primera_atencion': limpiar_fecha(row['Fecha_Primera_Atencion'])
                }
            )
        except Exception as e:
            print(f"Error al migrar diagnóstico {row['ID_Diagnostico']}: {str(e)}")
    print("Migración de Diagnósticos completada.")

def migrar_medicos(csv_path):
    print("Migrando Médicos...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            Medico.objects.get_or_create(
                id_medico=row['ID_Medico'],
                defaults={
                    'nombre': row['Nombre'],
                    'apellido_paterno': row['Apellido_Paterno'],
                    'apellido_materno': row['Apellido_Materno'],
                    'especialidad': row['Especialidad'],
                    'cedula_profesional': row['Cedula_Profesional'],
                    'celular': row['Celular'],
                    'telefono_consultorio': row['Telefono_Consultorio']
                }
            )
        except Exception as e:
            print(f"Error al migrar médico {row['ID_Medico']}: {str(e)}")
    print("Migración de Médicos completada.")

def migrar_informes_medicos(csv_path):
    print("Migrando Informes Médicos...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            diagnostico = Diagnostico.objects.get(id_diagnostico=row['ID_Diagnostico'])
            medico = Medico.objects.get(id_medico=row['Medico'])
            InformeMedico.objects.get_or_create(
                id_informe=row['ID_Informe'],
                defaults={
                    'id_diagnostico': diagnostico,
                    'fecha_informe': limpiar_fecha(row['Fecha_Informe']),
                    'medico': medico
                }
            )
        except Exception as e:
            print(f"Error al migrar informe médico {row['ID_Informe']}: {str(e)}")
    print("Migración de Informes Médicos completada.")

def migrar_facturas(csv_path):
    print("Migrando Facturas...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            Factura.objects.get_or_create(
                id_factura=row['ID_Factura'],
                defaults={
                    'id_reclamacion': row['ID_Reclamacion'],
                    'fecha': limpiar_fecha(row['Fecha']),
                    'subtotal': row['SubTotal'],
                    'moneda': row['Moneda'],
                    'tipo_cambio': row['TipoCambio'],
                    'total': row['Total'],
                    'metodo_pago': row['MetodoPago'],
                    'lugar_expedicion': row['LugarExpedicion'],
                    'nombre_emisor': row['Nombre_Emisor'],
                    'rfc_emisor': row['Rfc_Emisor'],
                    'domicilio_fiscal_receptor': row['DomicilioFiscalReceptor'],
                    'nombre_receptor': row['Nombre_Receptor'],
                    'rfc_receptor': row['Rfc_Receptor'],
                    'uuid': row['UUID']
                }
            )
        except Exception as e:
            print(f"Error al migrar factura {row['ID_Factura']}: {str(e)}")
    print("Migración de Facturas completada.")

def migrar_partidas_factura(csv_path):
    print("Migrando Partidas de Factura...")
    df = pd.read_csv(csv_path, encoding='latin1')
    for _, row in df.iterrows():
        try:
            factura = Factura.objects.get(id_factura=row['ID_Factura'])
            PartidaFactura.objects.get_or_create(
                id_partida=row['Id_Partida'],
                defaults={
                    'id_factura': factura,
                    'descripcion': row['Descripcion'],
                    'importe': row['Importe']
                }
            )
        except Exception as e:
            print(f"Error al migrar partida de factura {row['Id_Partida']}: {str(e)}")
    print("Migración de Partidas de Factura completada.")

def migrar_datos():
    try:
        # Ruta a los archivos CSV
        base_path = r'C:\Users\victo\Desktop\csv'  # Ajusta esta ruta según donde tengas tus archivos CSV
        
        # Migrar en orden para mantener las relaciones
        migrar_companias(os.path.join(base_path, 'companias.csv'))
        migrar_planes(os.path.join(base_path, 'planes.csv'))
        migrar_polizas(os.path.join(base_path, 'polizas.csv'))
        migrar_diagnosticos(os.path.join(base_path, 'diagnosticos.csv'))
        migrar_medicos(os.path.join(base_path, 'medicos.csv'))
        migrar_informes_medicos(os.path.join(base_path, 'informes_medicos.csv'))
        migrar_facturas(os.path.join(base_path, 'facturas.csv'))
        migrar_partidas_factura(os.path.join(base_path, 'partidas_factura.csv'))
        
        print("¡Migración completada exitosamente!")
        
    except Exception as e:
        print(f"Error durante la migración: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        import traceback
        print(f"Detalles del error:\n{traceback.format_exc()}")

if __name__ == '__main__':
    migrar_datos() 