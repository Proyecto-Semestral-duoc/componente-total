from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # Otras URL de tu aplicación aquí...
    
    # URL para la vista de inicio de sesión
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

    