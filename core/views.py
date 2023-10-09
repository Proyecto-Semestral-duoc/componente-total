from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse
from datetime import date

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
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def ver_carrito(request):
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtener los elementos del carrito para el usuario actual
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        # Si el usuario no está autenticado, mostrar un carrito vacío
        carrito_items = []

    return render(request, 'ver_carrito.html', {'carrito_items': carrito_items})


def agregar_al_carrito(request, producto_id):
    print(producto_id)
    # Obtener el producto que se desea agregar al carrito
    producto = Producto.objects.get(id=producto_id)

    if request.method == 'POST':
        # Si se envió un formulario, obtener la cantidad ingresada por el usuario
        cantidad = int(request.POST.get('cantidad', 1))
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Crear un nuevo elemento en el carrito para el usuario autenticado
            carrito_item, created = CarritoItem.objects.get_or_create(
                usuario=request.user,
                producto=producto
            )
            # Actualizar la cantidad en el carrito
            carrito_item.cantidad += cantidad
            carrito_item.save()
            messages.success(request, f'Se agregaron {cantidad} {producto.nombre} al carrito.')
        else:
            # Si el usuario no está autenticado, mostrar un mensaje de error
            messages.error(request, 'Debes iniciar sesión para agregar productos al carrito.')

    return redirect('home')  # Redirigir al usuario de vuelta a la página de inicio


def eliminar_item_del_carrito(request, item_id):
    # Busca el elemento del carrito por ID o muestra un error 404 si no se encuentra
    item = get_object_or_404(CarritoItem, id=item_id)

    # Elimina el elemento del carrito
    item.delete()

    # Redirige de nuevo a la página del carrito
    return redirect('ver_carrito') 
 # Cambia 'ver_carrito' al nombre de la URL de tu vista de carrito
def crear_orden_compra(request):
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        carrito_items = []

    total = 0
    for item in carrito_items:
        subtotal = item.producto.precio * item.cantidad
        total += subtotal

    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        print("1")
        if form.is_valid():
            print("2")
            telefono = form.cleaned_data['telefono']
            print(telefono)
            direccion = form.cleaned_data['direccion']
            print(direccion)
            comuna = form.cleaned_data['comuna']
            print(comuna)
            # Ahora puedes usar estos datos como desees, por ejemplo, guardarlos en el modelo OrdenCompra
            orden_compra = form.save(commit=False)
            orden_compra.valor = total
            print(total)
            orden_compra.usuario = request.user
            orden_compra.fecha = date.today()
            print(date.today())
            orden_compra.telefono = telefono  # Asigna el teléfono
            orden_compra.direccion = direccion  # Asigna la dirección
            orden_compra.comuna = comuna  # Asigna la comuna
            orden_compra.save() 
    # Agregar los productos del carrito a la orden de compra
            for item in carrito_items:
                orden_compra.productos.add(item.producto)

            orden_compra.save() 
            
            for item in carrito_items:
                item.delete()

            messages.success(request, 'La orden de compra se ha creado exitosamente.')
            return redirect('crear_orden')
    else:
        form = OrdenCompraForm()

    regiones = Region.objects.all()
    comunas = Comuna.objects.all()

    return render(request, 'crear_orden.html', {'form': form, 'regiones': regiones, 'comunas': comunas, 'carrito_items': carrito_items, 'total': total})

def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
    return JsonResponse(list(comunas), safe=False)
