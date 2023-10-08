from .models import *
from django import forms

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['direccion', 'telefono', 'comuna']