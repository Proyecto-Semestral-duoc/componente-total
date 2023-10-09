# componente-total

Nuestro proyecto, consiste en la creación de un sistema web el cual permita la venta de componentes de computadores mediante la creacion de ordenes de venta.

## Requisitos

Antes de comenzar, asegúrate de tener instalado Python y pip en tu sistema.

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Proyecto-Semestral-duoc/componente-total
```
2. Navega al directorio del proyecto:
```bash
cd componente-total
```
3. Instala las dependencias utilizando pip y el archivo requirements.txt:

```bash
pip install -r requirements.txt
```
4. Debes realizar las migraciones de la base de datos.
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Finalmente debes ejecutar el comando para que la pagina inicie
```bash
python manage.py runserver
```
   
# Contribuciones
Si deseas contribuir a este proyecto, sigue los siguientes pasos:

Haz un fork del proyecto
Crea una nueva rama (git checkout -b feature/nueva-caracteristica)
Haz tus cambios y haz commit (git commit -m 'Añade nueva característica')
Haz push a la rama (git push origin feature/nueva-caracteristica)
Abre un Pull Request


