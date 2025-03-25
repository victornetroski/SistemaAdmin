# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compania',
            fields=[
                ('id_aseguradora', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('nombre_corto', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AseguradoraPlan',
            fields=[
                ('id_plan', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('id_aseguradora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_asegurados.compania')),
            ],
        ),
        migrations.CreateModel(
            name='Poliza',
            fields=[
                ('id_poliza', models.AutoField(primary_key=True, serialize=False)),
                ('numero_poliza', models.CharField(max_length=100)),
                ('fisica_moral', models.CharField(choices=[('F', 'Fisica'), ('M', 'Moral')], max_length=1)),
                ('contratante_moral', models.CharField(blank=True, max_length=255, null=True)),
                ('folio_mercantil', models.CharField(blank=True, max_length=100, null=True)),
                ('objeto_social', models.TextField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido_paterno', models.CharField(max_length=255)),
                ('apellido_materno', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateField()),
                ('lugar_nacimiento', models.CharField(max_length=255)),
                ('curp', models.CharField(max_length=18)),
                ('pais_nacimiento', models.CharField(max_length=100)),
                ('nacionalidad', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=13)),
                ('profesion', models.CharField(max_length=255)),
                ('calle', models.CharField(max_length=255)),
                ('numero_exterior', models.CharField(max_length=50)),
                ('numero_interior', models.CharField(blank=True, max_length=50, null=True)),
                ('colonia', models.CharField(max_length=255)),
                ('municipio_delegacion', models.CharField(max_length=255)),
                ('entidad_federativa', models.CharField(max_length=255)),
                ('ciudad_poblacion', models.CharField(max_length=255)),
                ('codigo_postal', models.CharField(max_length=10)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('poliza_pdf', models.FileField(blank=True, null=True, upload_to='polizas/')),
                ('es_gobierno', models.BooleanField(default=False)),
                ('cargo', models.CharField(blank=True, max_length=255, null=True)),
                ('dependencia', models.CharField(blank=True, max_length=255, null=True)),
                ('actua_nombre_propio', models.BooleanField(default=True)),
                ('titular_contratante', models.CharField(blank=True, max_length=255, null=True)),
                ('clabe', models.CharField(blank=True, max_length=18, null=True)),
                ('banco', models.CharField(blank=True, max_length=100, null=True)),
                ('estado_cuenta_pdf', models.FileField(blank=True, null=True, upload_to='estados_cuenta/')),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('id_aseguradora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_asegurados.compania')),
                ('id_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_asegurados.aseguradoraplan')),
            ],
        ),
        migrations.CreateModel(
            name='Asegurado',
            fields=[
                ('id_asegurado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido_paterno', models.CharField(max_length=255)),
                ('apellido_materno', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], default='O', max_length=1)),
                ('rfc', models.CharField(blank=True, max_length=13, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('relacion', models.CharField(choices=[('T', 'Titular'), ('C', 'Conyuge'), ('D', 'Dependiente')], default='T', max_length=50)),
                ('iniciar_reclamo', models.BooleanField(default=False)),
                ('diagnostico', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('poliza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_asegurados.poliza')),
            ],
            options={
                'verbose_name': 'Asegurado',
                'verbose_name_plural': 'Asegurados',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id_diagnostico', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('diagnostico', models.TextField()),
                ('fecha_inicio_padecimiento', models.DateField()),
                ('fecha_primera_atencion', models.DateField()),
                ('id_asegurado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosticos_asegurado', to='gestion_asegurados.asegurado')),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id_medico', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido_paterno', models.CharField(max_length=255)),
                ('apellido_materno', models.CharField(max_length=255)),
                ('especialidad', models.CharField(max_length=255)),
                ('cedula_profesional', models.CharField(max_length=100)),
                ('celular', models.CharField(max_length=20)),
                ('telefono_consultorio', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InformeMedico',
            fields=[
                ('id_informe', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_informe', models.DateField()),
                ('pdf', models.FileField(upload_to='informes/')),
                ('id_diagnostico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_asegurados.diagnostico')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_asegurados.medico')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id_factura', models.AutoField(primary_key=True, serialize=False)),
                ('id_reclamacion', models.CharField(max_length=100)),
                ('archivo_pdf', models.FileField(upload_to='facturas/pdf/')),
                ('archivo_xml', models.FileField(upload_to='facturas/xml/')),
                ('archivo_desglose', models.FileField(blank=True, null=True, upload_to='facturas/desglose/')),
                ('fecha', models.DateField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('moneda', models.CharField(max_length=3)),
                ('tipo_cambio', models.DecimalField(decimal_places=4, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=100)),
                ('lugar_expedicion', models.CharField(max_length=255)),
                ('nombre_emisor', models.CharField(max_length=255)),
                ('rfc_emisor', models.CharField(max_length=13)),
                ('domicilio_fiscal_receptor', models.CharField(max_length=255)),
                ('nombre_receptor', models.CharField(max_length=255)),
                ('rfc_receptor', models.CharField(max_length=13)),
                ('uuid', models.CharField(max_length=36, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartidaFactura',
            fields=[
                ('id_partida', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_asegurados.factura')),
            ],
        ),
    ] 