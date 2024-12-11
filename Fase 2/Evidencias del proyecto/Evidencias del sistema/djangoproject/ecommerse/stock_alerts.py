from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Producto

@receiver(post_save, sender=Producto)
def verificar_stock_bajo(sender, instance, **kwargs):
    """
    Envía un correo si el stock actual de un producto es menor o igual al stock mínimo
    después de guardar el producto.
    """
    if instance.stock_actual <= instance.stock_minimo:
        mensaje = (
            f"El producto '{instance.nombre}' tiene stock bajo.\n"
            f"Stock actual: {instance.stock_actual}\n"
            f"Stock mínimo: {instance.stock_minimo}\n"
        )
        
        # Enviar correo de alerta
        send_mail(
            'Alerta: Producto con bajo stock',
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            ['ba.madrid@duocuc.cl'],  # Cambia a tu correo o una lista de correos
            fail_silently=False,
        )
