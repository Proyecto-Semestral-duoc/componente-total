from django.shortcuts import render
from .models import *
# Create your views here.

# Asegúrate de importar tu modelo de OrdenCompra

def listar_ordenes_compra(request):
    # Recupera todas las órdenes de compra almacenadas en la base de datos
    ordenes = OrdenCompra.objects.all()
    
    # Pasa las órdenes de compra al contexto para que estén disponibles en la plantilla
    return render(request, 'orden_compra.html', {'ordenes': ordenes})

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')