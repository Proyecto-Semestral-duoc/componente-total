from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse
from datetime import date
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import xlsxwriter
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from io import BytesIO


def es_superusuario(user):
    return user.is_superuser

# Asegúrate de importar tu modelo de OrdenCqompra
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

@user_passes_test(es_superusuario)
def generar_reporte(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        ordenes = OrdenCompra.objects.filter(fecha__range=[start_date, end_date])

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ordenes_compra.pdf"'

        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = f"Lista de reportes filtrados por {start_date} hasta {end_date}"
        elements.append(Paragraph(title, styles['Title']))

        data = [
            ['Nombre', 'Valor']
        ]

        for orden in ordenes:
            data.append(['Número de Factura:', str(orden.id_orden)])
            data.append(['Fecha:', str(orden.fecha)])
            data.append(['Valor total (con IVA):', orden.iva_orden()])  # Llama al método para obtener el valor
            data.append(['Dirección:', str(orden.direccion)])
            data.append(['Teléfono:', str(orden.telefono)])
            data.append(['Estado de Orden:', str(orden.get_estado_orden_display())])
            data.append(['', ''])  # Espacio entre cada orden

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        ordenes_table = Table(data)
        ordenes_table.setStyle(style)

        # Aplicar estilo específico a los elementos deseados
        for i in range(0, len(data), 2):
            if data[i][0] == 'Número de Factura:':
                # Aplicar estilo solo al primer elemento 'Número de Factura:'
                ordenes_table.setStyle(TableStyle([
                    ('FONTNAME', (0, i), (0, i), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, i), (0, i), 12),
                ]))
                break  # Salir del bucle después de aplicar el estilo al primer elemento

        elements.append(ordenes_table)

        pdf.build(elements)
        pdf_buffer = buffer.getvalue()
        buffer.close()

        response.write(pdf_buffer)
        return response

    return render(request, 'reporte.html')


@user_passes_test(es_superusuario)
def generar_reporte_excel(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        ordenes = OrdenCompra.objects.filter(fecha__range=[start_date, end_date])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="reporte_ordenes_compra.xlsx"'

        # Crear un nuevo libro y hoja de trabajo de Excel
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()

        # Establecer el formato para las celdas
        cell_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#D3D3D3',
                # Color de fondo similar al del PDF
        })

        # Aplicar borde negro a las celdas
        cell_format.set_border_color('black')

        # Encabezados de la tabla
        headers = ['Número de Orden', 'Usuario', 'Fecha', 'Valor total (con IVA)', 'Dirección', 'Teléfono', 'Estado de Orden']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, cell_format)

        # Escribir los datos de las órdenes en filas sucesivas
        row = 1
        for orden in ordenes:
            worksheet.write(row, 0, str(orden.id_orden))
            worksheet.write(row, 1, str(orden.usuario.username))
            worksheet.write(row, 2, str(orden.fecha.strftime('%Y-%m-%d')))
            worksheet.write(row, 3, orden.iva_orden())
            worksheet.write(row, 4, str(orden.direccion))
            worksheet.write(row, 5, str(orden.telefono))
            worksheet.write(row, 6, str(orden.get_estado_orden_display()))
            row += 1

        workbook.close()
        return response

    return render(request, 'reporte.html')


def visualizar_factura(request):
    user = request.user
    
    facturas = Factura.objects.all()
    if not user.is_superuser:
        facturas = Factura.objects.filter(orden_compra__usuario=user)
    
    return render(request, 'visualizar_factura.html', {'facturas': facturas})

@user_passes_test(es_superusuario)
def listar_modificar_orden(request):
    # Recupera todas las órdenes de compra almacenadas en la base de datos
    ordenes = OrdenCompra.objects.all()
    
    # Pasa las órdenes de compra al contexto para que estén disponibles en la plantilla
    return render(request, 'modificar_orden.html', {'ordenes': ordenes})

@user_passes_test(es_superusuario)
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

@user_passes_test(es_superusuario)
def listar_modificar_factura(request):
    # Recupera todas las facturas almacenadas en la base de datos
    facturas = Factura.objects.all()
    
    # Pasa las facturas al contexto para que estén disponibles en la plantilla
    return render(request, 'modificar_factura.html', {'facturas': facturas})


@user_passes_test(es_superusuario)
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

@user_passes_test(es_superusuario)
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

