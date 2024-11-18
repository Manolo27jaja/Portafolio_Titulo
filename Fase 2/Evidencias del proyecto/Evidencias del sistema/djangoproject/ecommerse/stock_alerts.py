from django.core.mail import send_mail
from django.conf import settings
from .models import Producto

def verificar_stock_bajo():
    productos_bajo_stock = Producto.objects.filter(stock_actual__lte=models.F('stock_minimo'))
    
    if productos_bajo_stock.exists():
        mensaje = "Los siguientes productos tienen stock bajo:\n"
        for producto in productos_bajo_stock:
            mensaje += f"{producto.nombre} (Stock actual: {producto.stock_actual})\n"
        
        # Enviar un correo electrónico de alerta (si es necesario)
        send_mail(
            'Alerta: Productos con bajo stock',
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [settings.bastianmandrid72@gmail.com],  # Cambia esto a tu correo de admin
            fail_silently=False,
        )
