from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

class OrdenCompraForm(forms.ModelForm):
    
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_region'}),  # Agregar clase 'form-control' para Bootstrap
    )

    direccion = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),  # Agregar clase 'form-control' para Bootstrap
    )

    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),  # Agregar clase 'form-control' para Bootstrap
    )

    class Meta:
        model = OrdenCompra
        fields = ['direccion', 'telefono', 'comuna']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'email', 'direccion']  # Los campos que se pueden modificar en el formulario

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requerido, ingrese una direccion de correo válida.')
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'fecha_nacimiento', 'direccion', 'nombre', 'apellido',  'password1', 'password2', )