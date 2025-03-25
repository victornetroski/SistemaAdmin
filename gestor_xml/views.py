from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import  XMLUploadForm
from .models import XMLFile
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import xml.etree.ElementTree as ET  # Para procesar XML
from reportlab.pdfgen import canvas  # Para generar PDFs
import logging
from xml.etree.ElementTree import ParseError
import os
from PyPDF2 import PdfReader, PdfWriter
from django.conf import settings
from .models import Comprobante, Emisor, Receptor, Concepto, Traslado, Impuestos, Complemento
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from gestor_documentos.models import Asegurado, Documento

logger = logging.getLogger(__name__)

# Create your views here.
def procesar_xml(file):
    try:
        # Intentar cargar y analizar el archivo XML
        tree = ET.parse(file)  # Esto carga el archivo XML en un árbol
        root = tree.getroot()  # Obtiene la raíz del árbol

        print("Estructura del XML:", ET.tostring(root, encoding='utf-8').decode('utf-8'))

        # Si llega aquí, el XML se cargó correctamente
        print("XML cargado correctamente.")

        # Declarar el namespace necesario (para manejar `tfd`)
        namespaces = {'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}

        # Buscar el nodo <tfd:TimbreFiscalDigital>
        timbre = root.find('.//tfd:TimbreFiscalDigital', namespaces)
        if timbre is not None:
            uuid = timbre.attrib.get('UUID', None)  # Extraer el valor de `UUID`
            if uuid:
                print(f"Valor de UUID extraído: {uuid}")
            else:
                print("No se encontró el atributo UUID.")
        else:
            print("No se encontró el nodo <tfd:TimbreFiscalDigital>.")

        return root
    except ET.ParseError as e:
        # Capturar errores relacionados con el formato del XML
        print(f"Error en el formato del XML: {e}")
        return None
    except Exception as e:
        # Capturar otros errores genéricos
        print(f"Error inesperado: {e}")
        return None

        
def extract_ns0_elements(root):
    # Inicializar un diccionario para almacenar etiquetas y atributos
    ns0_data = []

    # Definir el espacio de nombres (ajustar según el XML)
    namespaces = {'ns0': 'http://www.sat.gob.mx/cfd/4'}

    # Recorrer todos los nodos con el prefijo 'ns0:'
    for elem in root.iter():
        if elem.tag.startswith("{http://www.sat.gob.mx/cfd/4}"):
            # Obtener la etiqueta sin el espacio de nombres
            tag_name = elem.tag.split('}', 1)[1]
            # Obtener sus atributos
            ns0_data.append({tag_name: elem.attrib})

    return ns0_data



def extract_total(ns0_data):
    # Recorrer los datos y buscar el atributo 'Total' en la etiqueta 'Comprobante'
    for data in ns0_data:
        if 'Comprobante' in data:  # Verificar si el nodo es 'Comprobante'
            return data['Comprobante'].get('Total')  # Devolver el valor de 'Total'
    return None  # Retornar None si no se encuentra el atributo


def fill_pdf_template(pdf_template_path, response, total_value):
    try:
        # Verificar si el archivo existe
        if not os.path.exists(pdf_template_path):
            raise FileNotFoundError(f"No se encontró el archivo template: {pdf_template_path}")

        # Leer el PDF editable
        reader = PdfReader(pdf_template_path)
        writer = PdfWriter()

        # Listar todos los campos del formulario para depuración
        fields = reader.get_fields()
        logger.info(f"Campos disponibles en el formulario: {fields.keys()}")

        # Copiar páginas y rellenar el campo Total
        for page in reader.pages:
            writer.add_page(page)

        # Rellenar el campo 'Total' (ajustar según nombre del campo)
        writer.update_page_form_field_values(
            writer.pages[1],
            {"Text Field 599": str(total_value)}  # Convertir a string para asegurar compatibilidad
        )

        # Guardar el resultado directamente en la respuesta HTTP
        writer.write(response)
        
    except Exception as e:
        logger.error(f"Error al generar el PDF: {str(e)}")
        raise

from .models import Comprobante, Emisor, Receptor, Concepto, Traslado, Impuestos, Complemento

def guardar_datos_xml(root):
    namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/4', 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
    
    # Comprobante
    comprobante_attrib = root.attrib
    fecha = comprobante_attrib.get('Fecha')
    if fecha:
        fecha = make_aware(datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S'))
    comprobante = Comprobante.objects.create(
        version=comprobante_attrib.get('Version'),
        folio=comprobante_attrib.get('Folio'),
        fecha=fecha,
        forma_pago=comprobante_attrib.get('FormaPago'),
        no_certificado=comprobante_attrib.get('NoCertificado'),
        certificado=comprobante_attrib.get('Certificado'),
        subtotal=comprobante_attrib.get('SubTotal'),
        moneda=comprobante_attrib.get('Moneda'),
        exportacion=comprobante_attrib.get('Exportacion'),
        total=comprobante_attrib.get('Total'),
        tipo_comprobante=comprobante_attrib.get('TipoDeComprobante'),
        metodo_pago=comprobante_attrib.get('MetodoPago'),
        lugar_expedicion=comprobante_attrib.get('LugarExpedicion'),
        sello=comprobante_attrib.get('Sello')
    )

    # Emisor
    emisor = root.find('.//cfdi:Emisor', namespaces)
    if emisor is not None:
        Emisor.objects.create(
            comprobante=comprobante,
            rfc=emisor.attrib.get('Rfc'),
            nombre=emisor.attrib.get('Nombre'),
            regimen_fiscal=emisor.attrib.get('RegimenFiscal')
        )

    # Receptor
    receptor = root.find('.//cfdi:Receptor', namespaces)
    if receptor is not None:
        Receptor.objects.create(
            comprobante=comprobante,
            rfc=receptor.attrib.get('Rfc'),
            nombre=receptor.attrib.get('Nombre'),
            domicilio_fiscal=receptor.attrib.get('DomicilioFiscalReceptor'),
            regimen_fiscal_receptor=receptor.attrib.get('RegimenFiscalReceptor'),
            uso_cfdi=receptor.attrib.get('UsoCFDI')
        )

    # Conceptos
    conceptos = root.findall('.//cfdi:Concepto', namespaces)
    for concepto in conceptos:
        concepto_obj = Concepto.objects.create(
            comprobante=comprobante,
            objeto_imp=concepto.attrib.get('ObjetoImp'),
            clave_prod_serv=concepto.attrib.get('ClaveProdServ'),
            no_identificacion=concepto.attrib.get('NoIdentificacion'),
            cantidad=concepto.attrib.get('Cantidad'),
            clave_unidad=concepto.attrib.get('ClaveUnidad'),
            unidad=concepto.attrib.get('Unidad'),
            descripcion=concepto.attrib.get('Descripcion'),
            valor_unitario=concepto.attrib.get('ValorUnitario'),
            importe=concepto.attrib.get('Importe')
        )

        # Traslados
        traslados = concepto.findall('.//cfdi:Traslado', namespaces)
        for traslado in traslados:
            Traslado.objects.create(
                concepto=concepto_obj,
                impuesto=traslado.attrib.get('Impuesto'),
                base=traslado.attrib.get('Base'),
                tipo_factor=traslado.attrib.get('TipoFactor'),
                tasa_o_cuota=traslado.attrib.get('TasaOCuota'),
                importe=traslado.attrib.get('Importe')
            )

    # Impuestos
    impuestos = root.find('.//cfdi:Impuestos', namespaces)
    if impuestos is not None:
        Impuestos.objects.create(
            comprobante=comprobante,
            total_trasladados=impuestos.attrib.get('TotalImpuestosTrasladados')
        )

    # Complemento
    complemento = root.find('.//cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces)
    if complemento is not None:
        fecha_timbrado = complemento.attrib.get('FechaTimbrado')
        if fecha_timbrado:
            fecha_timbrado = make_aware(datetime.strptime(fecha_timbrado, '%Y-%m-%dT%H:%M:%S'))
        uuid = complemento.attrib.get('UUID')
        Complemento.objects.update_or_create(
            uuid=uuid,
            defaults={
                'comprobante': comprobante,
                'version': complemento.attrib.get('Version'),
                'fecha_timbrado': fecha_timbrado,
                'rfc_prov_certif': complemento.attrib.get('RfcProvCertif'),
                'sello_cfd': complemento.attrib.get('SelloCFD'),
                'no_certificado_sat': complemento.attrib.get('NoCertificadoSAT'),
                'sello_sat': complemento.attrib.get('SelloSAT'),
            }
        )
@login_required
def upload_xml(request):
    extracted_data = None  # Inicializar la variable para almacenar los datos extraídos

    if request.method == 'POST':
        try:
            form = XMLUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']

                # Validar si el archivo no está vacío
                if file.size == 0:
                    messages.error(request, "El archivo está vacío. Por favor, sube un archivo XML válido.")
                    return render(request, 'upload_xml.html', {'form': form})

                # Procesar el archivo XML
                root = procesar_xml(file)
                if root is None:
                    messages.error(request, "Error al procesar el archivo XML. Verifica el formato.")
                    return render(request, 'upload_xml.html', {'form': form})

                # Guardar los datos del XML en la base de datos
                guardar_datos_xml(root)
                messages.success(request, "Los datos del archivo XML se guardaron exitosamente.")

                # Extraer datos para mostrar en la plantilla
                namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/4'}
                comprobante_attrib = root.attrib

                extracted_data = {
                    'version': comprobante_attrib.get('Version'),
                    'folio': comprobante_attrib.get('Folio'),
                    'fecha': comprobante_attrib.get('Fecha'),
                    'forma_pago': comprobante_attrib.get('FormaPago'),
                    'total': comprobante_attrib.get('Total'),
                    'emisor': root.find('.//cfdi:Emisor', namespaces).attrib if root.find('.//cfdi:Emisor', namespaces) else {},
                    'receptor': root.find('.//cfdi:Receptor', namespaces).attrib if root.find('.//cfdi:Receptor', namespaces) else {},
                }

                # Guardar los datos para el siguiente paso (por ejemplo, generación del PDF)
                request.session['extracted_data'] = extracted_data  # Usar sesión para almacenar datos temporalmente

        except Exception as e:
            logger.error(f"Error durante el procesamiento: {e}")
            messages.error(request, "Ocurrió un error al procesar el archivo XML.")
            return render(request, 'upload_xml.html', {'form': form})

    else:
        form = XMLUploadForm()

    # Enviar el formulario y los datos extraídos al contexto
    return render(request, 'upload_xml.html', {'form': form, 'extracted_data': extracted_data})


@login_required
def generate_pdf(request, asegurado_id):
    try:
        # Obtener el asegurado
        asegurado = Asegurado.objects.get(id=asegurado_id, usuario=request.user)
        
        # Obtener el último documento XML del asegurado
        documento_xml = Documento.objects.filter(
            asegurado=asegurado,
            es_xml=True
        ).order_by('-fecha_subida').first()
        
        if not documento_xml:
            messages.error(request, 'No se encontró ningún documento XML para este asegurado.')
            return redirect('detalle_asegurado', asegurado_id=asegurado_id)
        
        # Obtener los datos del XML
        datos_xml = documento_xml.datos_xml
        if not datos_xml:
            messages.error(request, 'El documento XML no tiene datos procesados.')
            return redirect('detalle_asegurado', asegurado_id=asegurado_id)
        
        # Obtener el total del XML
        total = datos_xml.get('total')
        if not total:
            messages.error(request, 'No se encontró el total en el documento XML.')
            return redirect('detalle_asegurado', asegurado_id=asegurado_id)
        
        # Definir la ruta del template PDF
        pdf_template_path = os.path.join(settings.BASE_DIR, 'tasks', 'pdfs', 'BUPA_FORMATO_REEMBOLSO.pdf')
        
        # Verificar si el archivo existe
        if not os.path.exists(pdf_template_path):
            logger.error(f"No se encontró el archivo template en: {pdf_template_path}")
            messages.error(request, 'Error: No se encontró el template del PDF.')
            return redirect('detalle_asegurado', asegurado_id=asegurado_id)
        
        # Crear la respuesta HTTP con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{asegurado.id}.pdf"'
        
        # Rellenar el template del PDF con los datos
        fill_pdf_template(pdf_template_path, response, total)
        
        return response
        
    except Asegurado.DoesNotExist:
        messages.error(request, 'Asegurado no encontrado.')
        return redirect('lista_asegurados')
    except FileNotFoundError as e:
        logger.error(f"Error al encontrar el archivo template: {str(e)}")
        messages.error(request, 'Error: No se encontró el template del PDF.')
        return redirect('detalle_asegurado', asegurado_id=asegurado_id)
    except Exception as e:
        logger.error(f"Error al generar el PDF: {str(e)}")
        messages.error(request, f'Error al generar el PDF: {str(e)}')
        return redirect('detalle_asegurado', asegurado_id=asegurado_id)
