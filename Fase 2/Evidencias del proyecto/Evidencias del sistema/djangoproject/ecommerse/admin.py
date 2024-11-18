from django.contrib import admin
from .models import Producto, Usuario

# Register your models here.

admin.site.register(Usuario)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock_actual', 'stock_minimo', 'es_stock_bajo')
    list_filter = ('stock_actual',)

admin.site.register(Producto, ProductoAdmin)

#superuser manolo password 1234
# manuel 1234