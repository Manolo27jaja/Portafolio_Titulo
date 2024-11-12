from django.contrib import admin
from django.urls import path
from ecommerse.views import detalle_producto, agregar_producto, eliminar_producto, limpiar_carrito, restar_producto, home, buscar, modal, guardar_carrito, carritoid , eliminar_deseado, dashboard_admin
from ecommerse import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('buscar/', buscar, name='buscar'),
    path('', home, name='home'),
    path('detalle_producto/', detalle_producto, name='detalle_producto'),
    path('carritoid/<int:producto_id>/', carritoid, name='carritoid'),
    path('guardar_carrito/', guardar_carrito, name='guardar_carrito'),
    #Paths de Carrito de compras
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    path('miCarrito/', views.miCarrito, name="miCarrito"),
    path('miCarrito/', views.mostrar_carrito, name='miCarrito'),
    #Paths de Sistema Login
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('read_sesion/', views.read_ingreso , name='read_ingreso'),
    #Paths para el recuperar contraseña
    # URL para la vista de recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form_custom.html'), name='password_reset'),
    # URL que se mostrará después de enviar el formulario de recuperación
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_custom.html'), name='password_reset_done'),
    # URL para la vista que procesa el enlace enviado por correo
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm_custom.html'), name='password_reset_confirm'),
    # URL para la vista cuando la contraseña ha sido reseteada con éxito
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete_custom.html'), name='password_reset_complete'),


    # URL PARA deseados 
    path('deseados/', views.ver_deseados, name='ver_deseados'),  
    path('agregar_deseado/<int:producto_id>/', views.agregar_deseado, name='agregar_deseado'),
    path('deseados/', views.deseados, name='deseados'),
    path('eliminar_deseado/<int:deseado_id>/', eliminar_deseado, name='eliminar_deseado'),


    path('admin_dashboard/', dashboard_admin, name='dashboard_admin'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('dashboard-graficos/', views.dashboard_graficos, name='dashboard_graficos'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
