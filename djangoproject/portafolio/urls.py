from django.contrib import admin
from django.urls import path
from ecommerse.views import agregar_producto, eliminar_producto, limpiar_carrito, restar_producto, home, carrito, buscar, modal, guardar_carrito
from ecommerse import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', buscar, name='buscar'),
    path('', home, name='home'),
    path('modal/', modal, name='modal'),
    path('carrito/', carrito, name='carrito'),
    path('guardar_carrito/', guardar_carrito, name='guardar_carrito'),
    #Paths de Carrito de compras
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
    # URL para la vistas de pago aceptado o rechazado
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago-celular-bricks/', views.pago_celular_bricks, name='pago_celular_bricks'),
]

