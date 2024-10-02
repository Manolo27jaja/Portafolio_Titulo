"""
URL configuration for portafolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommerse.views import agregar_producto, eliminar_producto, limpiar_carrito, restar_producto, home, carrito, buscar#, obtener_carrito#, #read_carrito,
from ecommerse import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', buscar, name='buscar'),
    path('', home, name='home'),
    #path('carrito/', read_carrito, name='read_carrito'),
    path('carrito/', carrito, name='carrito'),
    #Paths de Carrito de compras
    #path('obtener_carrito/', obtener_carrito, name='obtener_carrito'),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    #Paths de Sistema Login
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('read_sesion/', views.read_ingreso , name='read_ingreso'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('registro/', views.registro, name='registro'),
    #Paths para el recuperar contraseña
    # URL para la vista de recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # URL que se mostrará después de enviar el formulario de recuperación
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # URL para la vista que procesa el enlace enviado por correo
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # URL para la vista cuando la contraseña ha sido reseteada con éxito
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

