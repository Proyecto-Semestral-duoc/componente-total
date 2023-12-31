# Generated by Django 4.2.3 on 2023-10-08 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_ordencompra'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_despacho', models.CharField(choices=[('rechazado', 'Rechazado'), ('pendiente', 'Pendiente'), ('despachado', 'Despachado')], default='pendiente', max_length=20)),
                ('orden_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ordencompra')),
            ],
        ),
    ]
