# templatetags/carrito_extras.py
from django import template

register = template.Library()

@register.filter
def get_total_carrito(carrito):
    total = 0
    for item in carrito.values():
        total += item['acumulado']
    return total

@register.filter
def dividir(valor1, valor2):
    if valor2 != 0:
        return valor1 / valor2
    return 0  # Evitar división por cero
