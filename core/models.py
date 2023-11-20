from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from decimal import Decimal
import random

class CustomUser(AbstractUser):
    # Agrega campos personalizados aquí
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)

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

class CarritoItem(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    def subtotal(self):
        return self.cantidad * self.producto.precio
        
    def costo_con_iva(self):
        subtotal = self.subtotal()
        iva = Decimal('0.19')
        return subtotal + (subtotal * iva)  # Calculamos el costo final con el 19% de IVA
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} para {self.usuario.username}"

class Region(models.Model):
    nombre = models.CharField(max_length=255, default='No seleccionado')

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=255, default='No seleccionado')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class OrdenBase(models.Model):
    id_orden = models.AutoField(primary_key=True)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True  # Esto hace que este modelo sea abstracto y no se cree una tabla en la base de datos

class OrdenCompra(OrdenBase):
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
    
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    def iva_orden(self):
        subtotal = self.valor
        iva = Decimal('0.19')
        total_con_iva = subtotal + (subtotal * iva)
        return f"${total_con_iva.quantize(Decimal('0.00'))}"  # Redondea a 0 decimales y agrega el signo de peso
    
    def __str__(self):
        return f'OrdenCompra #{self.id_orden}'



# Modelo para Factura que también hereda de OrdenBase
class Factura(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)  # Relación con OrdenCompra
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

    def __str__(self):
        return f'OrdenCompra #{self.orden_compra.id_orden}'


# Define la función para crear el usuario admin
def crear_usuario_admin(**kwargs):
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser(username='admin', password='123', fecha_nacimiento='2013-03-03', direccion='dadsadsa')
        print(" Usuario administrador creado exitosamente.")

# Registra la función con la señal post_migrate
@receiver(post_migrate)
def post_migrate_callback(sender, **kwargs):
    crear_usuario_admin(**kwargs)
    

User = get_user_model()

@receiver(post_migrate)
def create_normal_user(sender, **kwargs):
    try:
        user = User.objects.get(username='cliente')
    except User.DoesNotExist:
        # Crea un usuario normal si no existe
        user = User.objects.create_user(
            username='cliente',
            password='123',
            fecha_nacimiento='2013-03-03',
            direccion='dirección_normal'
        )
        print(" Usuario normal creado exitosamente.")




@receiver(post_migrate)
def crear_productos_de_prueba(sender, **kwargs):
    productos_de_prueba = [
    {
        'nombre': 'Laptop Acer Aspire 15"',
        'precio': 799.99,
        'descripcion': 'Laptop Acer Aspire con pantalla de 15", procesador Intel Core i5 y 8 GB de RAM.',
        'imagen': 'productos/producto.png'# Otras propiedades del producto 1''
    },
    {
        'nombre': 'Monitor Dell UltraSharp 27"',
        'precio': 349.99,
        'descripcion': 'Monitor Dell UltraSharp de 27" con resolución 4K y tecnología IPS.',
        'imagen': 'productos/producto2.jpg'# Otras propiedades del producto 2
    },
    {
        'nombre': 'Teclado Mecánico RGB',
        'precio': 89.99,
        'descripcion': 'Teclado mecánico RGB con retroiluminación personalizable y teclas programables.',
        'imagen': 'productos/producto3.png'# Otras propiedades del producto 3
    },
    {
        'nombre': 'Mouse Inalámbrico Logitech',
        'precio': 29.99,
        'descripcion': 'Mouse inalámbrico Logitech con sensor óptico y diseño ergonómico.',
        'imagen': 'productos/producto4.jpeg'# Otras propiedades del producto 4
    },
    {
        'nombre': 'Tarjeta Gráfica NVIDIA GeForce RTX 3080',
        'precio': 999.99,
        'descripcion': 'Tarjeta gráfica NVIDIA GeForce RTX 3080 con 10 GB de memoria GDDR6X.',
        'imagen': 'productos/producto5.jpeg'# Otras propiedades del producto 5
    },
    {
        'nombre': 'Disco Duro SSD Samsung 1TB',
        'precio': 149.99,
        'descripcion': 'Disco duro SSD Samsung de 1TB con velocidad de lectura/escritura rápida.',
        'imagen': 'productos/producto6.png'# Otras propiedades del producto 6
    },
    {
        'nombre': 'Impresora HP LaserJet Pro',
        'precio': 299.99,
        'descripcion': 'Impresora láser HP LaserJet Pro con impresión a color y escaneo.',
        'imagen': 'productos/producto7.jpeg'# Otras propiedades del producto 7
    },
    # Puedes agregar más productos de prueba según sea necesario
    ]
    if Producto.objects.count() == 0:
        print(" Ingresando productos por favor espere ...")
        for producto_data in productos_de_prueba:
            Producto.objects.get_or_create(**producto_data)


        print(" productos de prueba ingresados")

    data = [
    {
        "region": "Arica y Parinacota",
        "comunas": ["Arica", "Camarones", "Putre", "General Lagos"]
    },
    {
        "region": "Tarapacá",
        "comunas": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"]
    },
    {
        "region": "Antofagasta",
        "comunas": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "Tocopilla", "María Elena"]
    },
    {
        "region": "Atacama",
        "comunas": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Alto del Carmen", "Freirina", "Huasco"]
    },
    {
        "region": "Coquimbo",
        "comunas": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paiguano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"]
    },
    {
        "region": "Valparaíso",
        "comunas": ["Valparaíso", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví", "Quintero", "Viña del Mar", "Isla de Pascua", "Los Andes", "Calle Larga", "Rinconada", "San Esteban", "La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar", "Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales", "San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo", "San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María", "Quilpué", "Limache", "Olmué", "Villa Alemana"]
    },
    {
        "region": "Región del Libertador Gral. Bernardo O’Higgins",
        "comunas": ["Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente", "Pichilemu", "La Estrella", "Litueche", "Marchihue", "Navidad", "Paredones", "San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"]
    },
    {
        "region": "Región del Maule",
        "comunas": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Cauquenes", "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"]
    },
    {
        "region": "Región de Ñuble",
        "comunas": ["Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Quirihue", "Ránquil", "Treguaco", "Bulnes", "Chillán Viejo", "Chillán", "El Carmen", "Pemuco", "Pinto", "Quillón", "San Ignacio", "Yungay", "Coihueco", "Ñiquén", "San Carlos", "San Fabián", "San Nicolás"]
    },
    {
        "region": "Región del Biobío",
        "comunas": ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén", "Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa", "Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"]
    },
    {
        "region": "Región de la Araucanía",
        "comunas": ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"]
    },
    {
        "region": "Región de Los Ríos",
        "comunas": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco", "Río Bueno"]
    },
    {
        "region": "Región de Los Lagos",
        "comunas": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo", "Chaitén", "Futaleufú", "Hualaihué", "Palena"]
    },
    {
        "region": "Región Aisén del Gral. Carlos Ibáñez del Campo",
        "comunas": ["Coihaique", "Lago Verde", "Aisén", "Cisnes", "Guaitecas", "Cochrane", "O’Higgins", "Tortel", "Chile Chico", "Río Ibáñez"]
    },
    {
        "region": "Región de Magallanes y de la Antártica Chilena",
        "comunas": ["Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio", "Cabo de Hornos (Ex Navarino)", "Antártica", "Porvenir", "Primavera", "Timaukel", "Natales", "Torres del Paine"]
    },
    {
        "region": "Región Metropolitana de Santiago",
        "comunas": ["Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "Santiago", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil", "San Bernardo", "Buin", "Calera de Tango", "Paine", "Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"]
     },
    ]
    if Comuna.objects.count() == 0:
        print(" Ingresando regiones por favor espere ...")
        for item in data:
            region, created = Region.objects.get_or_create(nombre=item['region'])
            for comuna_nombre in item['comunas']:
                comuna, created = Comuna.objects.get_or_create(nombre=comuna_nombre, region=region)
        print(" regiones agregadas correctamente")
    

