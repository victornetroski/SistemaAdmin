import os
import django
import pandas as pd
from datetime import datetime
from django.core.files import File

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

def migrar_companias(df):
    print("Migrando Compañías...")
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

def migrar_planes(df):
    print("Migrando Planes...")
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

def migrar_polizas(df):
    print("Migrando Pólizas...")
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

def migrar_diagnosticos(df):
    print("Migrando Diagnósticos...")
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

def migrar_medicos(df):
    print("Migrando Médicos...")
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

def migrar_informes_medicos(df):
    print("Migrando Informes Médicos...")
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

def migrar_facturas(df):
    print("Migrando Facturas...")
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

def migrar_partidas_factura(df):
    print("Migrando Partidas de Factura...")
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
            print(f"Error al migrar partida {row['Id_Partida']}: {str(e)}")
    print("Migración de Partidas de Factura completada.")

def migrar_datos():
    try:
        ruta_excel = r'C:\Users\victo\Desktop\Asegurados.xlsx'
        print(f"Intentando leer el archivo Excel: {ruta_excel}")
        
        # Configuración específica para manejar la codificación
        excel_options = {
            'engine': 'openpyxl',
            'encoding': 'latin1',  # Probamos con latin1 para caracteres especiales
            'encoding_errors': 'replace'  # Reemplaza caracteres que no se pueden decodificar
        }

        # Leer cada hoja del Excel
        print("Leyendo hojas del archivo Excel...")
        
        if 'Compañias' in pd.ExcelFile(ruta_excel).sheet_names:
            df_companias = pd.read_excel(ruta_excel, sheet_name='Compañias', **excel_options)
            migrar_companias(df_companias)
        
        if 'Aseguradoras_Planes' in pd.ExcelFile(ruta_excel).sheet_names:
            df_planes = pd.read_excel(ruta_excel, sheet_name='Aseguradoras_Planes', **excel_options)
            migrar_planes(df_planes)
        
        if 'Poliza' in pd.ExcelFile(ruta_excel).sheet_names:
            df_polizas = pd.read_excel(ruta_excel, sheet_name='Poliza', **excel_options)
            migrar_polizas(df_polizas)
        
        if 'Diagnosticos' in pd.ExcelFile(ruta_excel).sheet_names:
            df_diagnosticos = pd.read_excel(ruta_excel, sheet_name='Diagnosticos', **excel_options)
            migrar_diagnosticos(df_diagnosticos)
        
        if 'Medicos' in pd.ExcelFile(ruta_excel).sheet_names:
            df_medicos = pd.read_excel(ruta_excel, sheet_name='Medicos', **excel_options)
            migrar_medicos(df_medicos)
        
        if 'Informes_Medicos' in pd.ExcelFile(ruta_excel).sheet_names:
            df_informes = pd.read_excel(ruta_excel, sheet_name='Informes_Medicos', **excel_options)
            migrar_informes_medicos(df_informes)
        
        if 'Facturas' in pd.ExcelFile(ruta_excel).sheet_names:
            df_facturas = pd.read_excel(ruta_excel, sheet_name='Facturas', **excel_options)
            migrar_facturas(df_facturas)
        
        if 'Partidas_Factura' in pd.ExcelFile(ruta_excel).sheet_names:
            df_partidas = pd.read_excel(ruta_excel, sheet_name='Partidas_Factura', **excel_options)
            migrar_partidas_factura(df_partidas)
        
        print("Migración completada exitosamente!")
        
    except Exception as e:
        print(f"Error durante la migración: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        import traceback
        print(f"Detalles del error:\n{traceback.format_exc()}")

if __name__ == '__main__':
    migrar_datos() 