from django.contrib.auth.models import AbstractUser
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre
    


class CustomUser(AbstractUser):
    # Agrega campos personalizados aquí
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.username
    

class Factura(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=255)
    
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

    def __str__(self):
        return self.numero_factura