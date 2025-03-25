import pandas as pd
import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')
django.setup()

from gestion_asegurados.models import Asegurado

def migrar_datos():
    try:
        # Leer el archivo Excel
        print("Iniciando proceso de migración...")
        print("Leyendo archivo Excel...")
        df = pd.read_excel('C:\\Users\\victo\\Desktop\\Asegurados.xlsx', encoding='utf-8')
        print(f"Total de filas en Excel: {len(df)}")
        
        # Mapeo de columnas de Excel a campos del modelo
        mapeo_campos = {
            'ID Asegurado': 'id_asegurado',
            'ID Póliza': 'id_poliza',
            'Nombre': 'nombre',
            'Apellido Paterno': 'apellido_paterno',
            'Apellido Materno': 'apellido_materno',
            'Fecha de Nacimiento': 'fecha_nacimiento',
            'Género': 'genero',
            'RFC': 'rfc',
            'Email': 'email',
            'Teléfono': 'telefono',
            'Titular/Cónyuge/Dependiente': 'titulat_conyuge_dependiente',
            'Iniciar Reclamo': 'iniciar_reclamo',
            'Diagnóstico': 'diagnostico',
            'Número Factura 1': 'numero_factura1',
            'Importe Factura 1': 'importe_factura1',
            'Día 1': 'dia1',
            'Día 2': 'dia2',
            'Mes 1': 'mes1',
            'Mes 2': 'mes2',
            'Año 1': 'año1',
            'Año 2': 'año2',
            'Año 3': 'año3',
            'Año 4': 'año4'
        }

        # Contadores
        creados = 0
        actualizados = 0
        errores = 0

        # Procesar cada fila del Excel
        for index, row in df.iterrows():
            try:
                # Crear diccionario con los datos mapeados
                datos_asegurado = {}
                for col_excel, campo_modelo in mapeo_campos.items():
                    if col_excel in row:
                        valor = row[col_excel]
                        
                        # Convertir tipos de datos según sea necesario
                        if campo_modelo == 'fecha_nacimiento' and pd.notna(valor):
                            if isinstance(valor, str):
                                try:
                                    valor = datetime.strptime(valor, '%Y-%m-%d').date()
                                except ValueError:
                                    try:
                                        valor = datetime.strptime(valor, '%d/%m/%Y').date()
                                    except ValueError:
                                        print(f"Error al convertir fecha en fila {index}: {valor}")
                                        valor = None
                            elif isinstance(valor, pd.Timestamp):
                                valor = valor.date()
                        
                        elif campo_modelo == 'iniciar_reclamo':
                            valor = bool(valor)
                        
                        elif campo_modelo == 'importe_factura1' and pd.notna(valor):
                            try:
                                valor = float(valor)
                            except (ValueError, TypeError):
                                print(f"Error al convertir importe en fila {index}: {valor}")
                                valor = None
                        
                        elif campo_modelo in ['dia1', 'dia2', 'mes1', 'mes2', 'año1', 'año2', 'año3', 'año4']:
                            if pd.notna(valor):
                                try:
                                    valor = int(valor)
                                except (ValueError, TypeError):
                                    print(f"Error al convertir número en fila {index}: {valor}")
                                    valor = None
                            else:
                                valor = None
                        
                        datos_asegurado[campo_modelo] = valor

                # Crear o actualizar el asegurado
                asegurado, creado = Asegurado.objects.update_or_create(
                    id_asegurado=datos_asegurado.get('id_asegurado'),
                    defaults=datos_asegurado
                )
                
                if creado:
                    creados += 1
                else:
                    actualizados += 1
                    
                print(f"Procesado: {datos_asegurado.get('id_asegurado')} - {'Creado' if creado else 'Actualizado'}")
                
            except Exception as e:
                errores += 1
                print(f"Error al procesar fila {index}: {str(e)}")
                continue

        print("\nResumen de la migración:")
        print(f"Total de registros procesados: {len(df)}")
        print(f"Registros creados: {creados}")
        print(f"Registros actualizados: {actualizados}")
        print(f"Errores encontrados: {errores}")
        
        # Verificar total en la base de datos
        total_bd = Asegurado.objects.count()
        print(f"\nTotal de registros en la base de datos: {total_bd}")
        
    except Exception as e:
        print(f"Error general en la migración: {str(e)}")

if __name__ == "__main__":
    migrar_datos() 