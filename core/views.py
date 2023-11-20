from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse
from datetime import date


# Create your views here.

# Asegúrate de importar tu modelo de OrdenCompra
def registro(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al usuario a la página de inicio de sesión después de registrarse
    else:
        form = SignUpForm()
    return render(request, 'registro.html', {'form': form})


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

def listar_modificar_orden(request):
    # Recupera todas las órdenes de compra almacenadas en la base de datos
    ordenes = OrdenCompra.objects.all()
    
    # Pasa las órdenes de compra al contexto para que estén disponibles en la plantilla
    return render(request, 'modificar_orden.html', {'ordenes': ordenes})

def modificar_estado_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra, id_orden=orden_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        orden.estado_orden = nuevo_estado
        orden.save()
        
        if nuevo_estado == 'aprobado':
            # Verifica si la orden ya tiene una factura asociada
            if not Factura.objects.filter(orden_compra=orden).exists():
                factura = Factura()
                factura.orden_compra = orden  # Puedes establecer el estado de despacho como desees
                factura.save()

    return redirect('listar_modificar_orden') # Redirige a la lista de órdenes de compra

def listar_modificar_factura(request):
    # Recupera todas las facturas almacenadas en la base de datos
    facturas = Factura.objects.all()
    
    # Pasa las facturas al contexto para que estén disponibles en la plantilla
    return render(request, 'modificar_factura.html', {'facturas': facturas})


def modificar_estado_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        factura.estado_despacho = nuevo_estado
        factura.save()

    return redirect('listar_modificar_factura')

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
    
    # Calcular el costo total con IVA
    total_con_iva = sum(item.costo_con_iva() for item in carrito_items)

    return render(request, 'ver_carrito.html', {'carrito_items': carrito_items, 'total_con_iva': total_con_iva})


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
            if not created:
                carrito_item.cantidad += cantidad
            else:
                carrito_item.cantidad = cantidad
            carrito_item.save()
            messages.success(request, f'Se agregaron {cantidad} {producto.nombre} al carrito.')
        else:
            # Si el usuario no está autenticado, mostrar un mensaje de error
            messages.error(request, 'Debes iniciar sesión para agregar productos al carrito.')

    return redirect('home')  # Redirigir al usuario de vuelta a la página de inicio


def eliminar_item_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)

    # Reducir la cantidad del elemento del carrito
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()

    return redirect('ver_carrito')

def eliminar_todos_items_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    CarritoItem.objects.filter(producto=item.producto).delete()
    return redirect('ver_carrito')

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


def modificar_despacho(request, factura_id):
    factura = Factura.objects.get(pk=factura_id)

    if request.method == 'POST':
        nuevo_estado_despacho = request.POST.get('nuevo_estado_despacho')
        factura.estado_despacho = nuevo_estado_despacho
        factura.save()

        # Opción 1: Redirigir al usuario después de guardar
        # return redirect('pagina_de_confirmacion')

        # Opción 2: Devolver una respuesta JSON para actualizar el modal
        response_data = {'success': True}
        return JsonResponse(response_data)

    # Si la solicitud es GET, simplemente renderiza la plantilla nuevamente
    context = {'factura': factura}
    return render(request, 'modificar_factura.html', context)

def perfil(request):
    # Obtener el usuario autenticado
    usuario = request.user
    
    # Renderizar la plantilla con los datos del usuario
    return render(request, 'perfil.html', {'usuario': usuario})

def modificar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige a la página del perfil después de guardar los cambios
    else:
        form = CustomUserForm(instance=usuario)
    
    return render(request, 'modificar_perfil.html', {'form': form})

