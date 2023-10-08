from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
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
    return redirect('ver_carrito')  # Cambia 'ver_carrito' al nombre de la URL de tu vista de carrito

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
        if form.is_valid():
            orden_compra = form.save(commit=False)
            

            
            orden_compra.valor = total
            orden_compra.usuario = request.user
            orden_compra.save()
            
            request.session['carrito'] = {}
            
            messages.success(request, 'La orden de compra se ha creado exitosamente.')
            return redirect('nombre_de_tu_vista_de_carrito')
    else:
        form = OrdenCompraForm()
    
    comunas = Comuna.objects.all()

    return render(request, 'crear_orden.html', {'form': form, 'comunas': comunas, 'carrito_items' : carrito_items, 'total': total})