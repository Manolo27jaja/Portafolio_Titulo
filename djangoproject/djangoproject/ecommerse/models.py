from django.db import models

# Aqui se crea la base de datos
# Crea la base de datos del carrito de compras, una base de datos basica para hacer funcionar funcionalidades.
class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=32)
    precio = models.IntegerField()
    imagen = models.ImageField()
    descripcion = models.CharField(max_length=255, default='Descripción por defecto')

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'