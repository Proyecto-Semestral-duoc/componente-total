from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from decimal import Decimal
import random

class CustomUser(AbstractUser):
    # Agrega campos personalizados aquí
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.username
    



def default_imagen_producto():
    return "productos/default.jpg"



class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/',default=default_imagen_producto)

    def __str__(self):
        return self.nombre
    
@receiver(post_migrate)
def crear_productos_de_prueba(sender, **kwargs):
    if sender.name == 'core':  # Reemplaza 'mi_app' con el nombre de tu aplicación
        # Crear productos de prueba en el evento post_migrate
        productos_de_prueba = [
        {
            'nombre': 'Laptop Acer Aspire 15"',
            'precio': 799.99,
            'descripcion': 'Laptop Acer Aspire con pantalla de 15", procesador Intel Core i5 y 8 GB de RAM.',
            # Otras propiedades del producto 1
        },
        {
            'nombre': 'Monitor Dell UltraSharp 27"',
            'precio': 349.99,
            'descripcion': 'Monitor Dell UltraSharp de 27" con resolución 4K y tecnología IPS.',
            # Otras propiedades del producto 2
        },
        {
            'nombre': 'Teclado Mecánico RGB',
            'precio': 89.99,
            'descripcion': 'Teclado mecánico RGB con retroiluminación personalizable y teclas programables.',
            # Otras propiedades del producto 3
        },
        {
            'nombre': 'Mouse Inalámbrico Logitech',
            'precio': 29.99,
            'descripcion': 'Mouse inalámbrico Logitech con sensor óptico y diseño ergonómico.',
            # Otras propiedades del producto 4
        },
        {
            'nombre': 'Tarjeta Gráfica NVIDIA GeForce RTX 3080',
            'precio': 999.99,
            'descripcion': 'Tarjeta gráfica NVIDIA GeForce RTX 3080 con 10 GB de memoria GDDR6X.',
            # Otras propiedades del producto 5
        },
        {
            'nombre': 'Disco Duro SSD Samsung 1TB',
            'precio': 149.99,
            'descripcion': 'Disco duro SSD Samsung de 1TB con velocidad de lectura/escritura rápida.',
            # Otras propiedades del producto 6
        },
        {
            'nombre': 'Impresora HP LaserJet Pro',
            'precio': 299.99,
            'descripcion': 'Impresora láser HP LaserJet Pro con impresión a color y escaneo.',
            # Otras propiedades del producto 7
        },
        # Puedes agregar más productos de prueba según sea necesario
    ]

        for producto_data in productos_de_prueba:
            Producto.objects.get_or_create(**producto_data)


    


class Region(models.Model):
    nombre = models.CharField(max_length=255, default='No seleccionado')

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=255, default='No seleccionado')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, blank=True)  # Campo para el teléfono
    ESTADO_DESPACHO_CHOICES = (
        ('rechazado', 'Rechazado'),
        ('pendiente', 'Pendiente'),
        ('despachado', 'Despachado'),
    )
    estado_despacho = models.CharField(
        max_length=20,
        choices=ESTADO_DESPACHO_CHOICES,
        default='pendiente',
    )

    # Relaciones
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    comuna = models.OneToOneField(Comuna, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.numero_factura
    
# <<<<<<< Updated upstream
# @receiver(post_migrate)
# def crear_facturas_de_ejemplo(sender, **kwargs):
#     if sender.name == 'core':  # Reemplaza 'mi_app' con el nombre de tu aplicación
#         if not CustomUser.objects.filter(username='admin').exists():
#             admin_user = CustomUser.objects.create_superuser(username='admin', password='123')
#             productos_de_prueba = list(Producto.objects.all())  # Convierte la lista de productos en una lista de objetos Producto

#             # Crear facturas de ejemplo
#             for i in range(5):  # Crear 5 facturas de ejemplo
#                 factura = Factura(
#                     numero_factura=f'FAC-{i+1}',
#                     fecha='2023-10-03',  # Reemplaza con la fecha deseada
#                     valor=sum(random.choice(productos_de_prueba).precio for _ in range(random.randint(1, 5))),  # Valor aleatorio basado en productos
#                     direccion='Dirección de ejemplo',
#                     usuario=admin_user,
#                     estado_despacho=random.choice(['rechazado', 'pendiente', 'despachado']),
#                 )
#                 factura.save()
#                 factura.productos.set(random.sample(productos_de_prueba, random.randint(1, 5)))  # Productos aleatorios
#                 print("Base de datos Lista")
#         else:
#             print("Base de datos ya rellenada")
# =======
class OrdenCompra(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    ESTADO_ORDEN_CHOICES = (
        ('rechazado', 'Rechazado'),
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
    )
    estado_orden = models.CharField(
        max_length=20,
        choices=ESTADO_ORDEN_CHOICES,
        default='pendiente',
    )

    # Relaciones
    comuna = models.OneToOneField(Comuna, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.numero_factura
