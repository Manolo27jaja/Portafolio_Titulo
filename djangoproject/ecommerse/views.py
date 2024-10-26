from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
# Bloque de importaciones del sistema login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
# Bloque de importaciones del carrito
from ecommerse.CarritoClass import CarritoClass
# Bloque de importaciones del modelo de base de datos
from ecommerse.models import Producto, Carrito, CarritoItem, Usuario
from .models import Usuario

def home(request):
    producto_ids_1 = [1, 2, 3, 4, 5, 6]  # Primer conjunto de productos
    producto_ids_2 = [7, 8, 9, 10, 11, 12]  # Segundo conjunto de productos para el otro carrusel
    productos_1 = Producto.objects.filter(id__in=producto_ids_1)
    productos_2 = Producto.objects.filter(id__in=producto_ids_2)
    por_categorias_1 = Producto.objects.filter(categoria="Consola")[:4]
    por_categorias_2 = Producto.objects.filter(categoria="Computadores")[:4]
    return render(request, 'home.html', {"productos_1": productos_1, "productos_2": productos_2, "por_categorias_1": por_categorias_1, "por_categorias_2": por_categorias_2})
#_________________________________________________

def carritoid(request, producto_id):
    producto_d = Producto.objects.filter(id=producto_id)
    return render(request, 'carrito.html', {"productos":producto_d})

@login_required
def guardar_carrito(request):
    if request.method == 'POST':
        # Recuperar el carrito desde la sesión
        carrito_session = request.session.get('carrito', {})
        if not carrito_session:
            return redirect('home')  # Si no hay nada en el carrito, redirigir
        # Crear un nuevo objeto de carrito en la base de datos
        carrito = Carrito.objects.create(usuario=request.user)
        # Guardar cada producto en CarritoItem
        for key, value in carrito_session.items():
            CarritoItem.objects.create(
                carrito=carrito,
                producto_id=value['producto_id'],
                cantidad=value['cantidad'],
                precio=value['acumulado'],
            )
        # Limpiar el carrito de la sesión después de guardarlo
        request.session['carrito'] = {}
        request.session.modified = True
        return redirect('home')
    
#_______________________________________________________

#____________________________________________________
# def read_carrito(request):
#     return render(request, 'carrito.html')

def read_ingreso(request):
    return render(request, 'inicio_sesion.html')

def agregar_producto(request, producto_id):
    carrito = CarritoClass(request)
    #producto = get_object_or_404(Producto, id=producto_id)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect('carritoid', producto_id=producto.id) #minuto 4:37 segunda parte del video

def eliminar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('carritoid', producto_id=producto.id)

def restar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect('carritoid', producto_id=producto.id)

def limpiar_carrito(request):
    carrito = CarritoClass(request)
    carrito.limpiar()
    return redirect('carritoid')

#_____________________________________________________

def buscar(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda desde la URL
    resultados = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.none()
    return render(request, 'buscar.html', {'resultados': resultados, 'query': query})

#____________________________________________________
# Metodos de sistema login

#def home(request):
 #   return render(request, 'home.html')

#____________________________________________________

def modal(request):
   return render(request, 'modal.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'crear_cuenta.html', {'form': form})

def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def recuperar(request):
    return render(request, 'recuperar.html')


def perfil(request):
    return render(request, 'perfil_usuario.html')

# def generar_buy_order():
#     return str(uuid.uuid4())

# def generar_session_id():
#     return str(uuid.uuid4())

#____________________________________________________________