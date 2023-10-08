# Generated by Django 4.2.3 on 2023-10-08 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_ordencompra_comuna_delete_factura_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id_orden', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
                ('estado_orden', models.CharField(choices=[('rechazado', 'Rechazado'), ('pendiente', 'Pendiente'), ('aprobado', 'Aprobado')], default='pendiente', max_length=20)),
                ('comuna', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.comuna')),
                ('productos', models.ManyToManyField(to='core.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]