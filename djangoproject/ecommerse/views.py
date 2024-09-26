from django.shortcuts import redirect, render, HttpResponse
from ecommerse.Carrito import Carrito
from ecommerse.models import Producto

#def home(request):
 #   producto_ids = [12, 9, 3, 4, 5, 11]  # Reemplaza con los IDs específicos
  #  productos = Producto.objects.filter(id__in=producto_ids)
   # return render(request, 'home.html', {"productos": productos})

def carrito(request):
    productos = Producto.objects.all()
    return render(request, 'carrito.html', {"productos":productos})

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect('carrito') #minuto 4:37 segunda parte del video

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('carrito')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect('carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('carrito') 