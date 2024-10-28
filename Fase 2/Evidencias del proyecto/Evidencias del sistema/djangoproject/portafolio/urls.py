from django.contrib import admin
from django.urls import path
<<<<<<< HEAD:djangoproject/portafolio/urls.py
from ecommerse.views import agregar_producto, eliminar_producto, limpiar_carrito, restar_producto, home, carrito, buscar, modal, guardar_carrito ,agregar_deseado,  eliminar_deseado , mostrar_producto_carrito   # Importa la nueva vista
=======
from ecommerse.views import agregar_producto, eliminar_producto, limpiar_carrito, restar_producto, home, buscar, modal, guardar_carrito, carritoid
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/portafolio/urls.py
from ecommerse import views
from django.contrib.auth import views as auth_views
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static

=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', buscar, name='buscar'),
    path('', home, name='home'),
    path('modal/', modal, name='modal'),
    path('carritoid/<int:producto_id>/', carritoid, name='carritoid'),
    path('guardar_carrito/', guardar_carrito, name='guardar_carrito'),
    # Paths de Carrito de compras
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
<<<<<<< HEAD:djangoproject/portafolio/urls.py
    # Paths de Sistema Login
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('read_sesion/', views.read_ingreso, name='read_ingreso'),
=======
<<<<<<< HEAD
    path('miCarrito/', views.miCarrito, name="miCarrito"),
    path('miCarrito/', views.mostrar_carrito, name='miCarrito'),
=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
    #Paths de Sistema Login
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('read_sesion/', views.read_ingreso , name='read_ingreso'),
<<<<<<< HEAD
    #Paths para el recuperar contraseña
    # URL para la vista de recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form_custom.html'), name='password_reset'),
    # URL que se mostrará después de enviar el formulario de recuperación
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_custom.html'), name='password_reset_done'),
    # URL para la vista que procesa el enlace enviado por correo
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm_custom.html'), name='password_reset_confirm'),
    # URL para la vista cuando la contraseña ha sido reseteada con éxito
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_custom.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/portafolio/urls.py
    path('recuperar/', views.recuperar, name='recuperar'),
    # Paths para recuperar contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('producto-carrito/', views.mostrar_producto_carrito, name='mostrar_producto_carrito'),


    path('deseados/', views.ver_deseados, name='ver_deseados'),  # Asegúrate de que este nombre coincida
    path('agregar_deseado/<int:producto_id>/', views.agregar_deseado, name='agregar_deseado'),
    path('eliminar_deseado/<int:producto_id>/', views.eliminar_deseado, name='eliminar_deseado'),
     path('deseados/', views.deseados, name='deseados'),



]

<<<<<<< HEAD:djangoproject/portafolio/urls.py



=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/portafolio/urls.py
