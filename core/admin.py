from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Producto)
admin.site.register(Factura)
admin.site.register(OrdenCompra)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(CustomUser)