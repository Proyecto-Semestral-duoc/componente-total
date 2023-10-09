from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Otras URL de tu aplicación aquí...
    # URL para la página de inicio
    path('', views.home, name='home'),
    # URL para la vista de inicio de sesión
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_item/<int:item_id>/', views.eliminar_item_del_carrito, name='eliminar_item'),
    path('crear_orden/', views.crear_orden_compra, name='crear_orden'),
    # URL para visualizar facturas
    path('visualizar_factura/', views.visualizar_factura, name='visualizar_factura'),

    # URL para listar las órdenes de compra
    path('orden_compra/', views.listar_ordenes_compra, name='orden_compra'),


    path('listar_modificar_factura/', views.listar_modificar_factura, name='listar_modificar_factura'),
    path('modificar_estado_factura/<int:factura_id>/', views.modificar_estado_factura, name='modificar_estado_factura'),
    path('listar_modificar_orden/', views.listar_modificar_orden, name='listar_modificar_orden'),
    path('modificar_estado_orden/<int:orden_id>/', views.modificar_estado_orden, name='modificar_estado_orden'),

    path('obtener_comunas/', views.obtener_comunas, name='obtener_comunas'),
    # URL para modificar facturas
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

