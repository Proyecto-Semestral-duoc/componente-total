from django.shortcuts import render
from .models import *
# Create your views here.

# Asegúrate de importar tu modelo de OrdenCompra

def listar_ordenes_compra(request):
    user = request.user
    ordenes = OrdenCompra.objects.all()
    
    if not user.is_superuser:
        ordenes = ordenes.filter(usuario=user)
    
    return render(request, 'orden_compra.html', {'ordenes': ordenes})

def visualizar_factura(request):
    user = request.user
    
    facturas = Factura.objects.all()
    if not user.is_superuser:
        facturas = Factura.objects.filter(orden_compra__usuario=user)
    
    return render(request, 'visualizar_factura.html', {'facturas': facturas})

def home(request):
    # Puedes agregar lógica adicional aquí para obtener productos u otra información que desees mostrar en la página de inicio.
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')