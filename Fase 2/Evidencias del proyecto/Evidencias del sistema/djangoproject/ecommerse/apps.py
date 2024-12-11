from django.apps import AppConfig


class EcommerseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerse'

    def ready(self):
        import ecommerse.stock_alerts  # Importa el archivo donde definiste la señal
