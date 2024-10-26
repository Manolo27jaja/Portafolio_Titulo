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

def carrito(request):
    producto_ids_1 = [5]  # Primer conjunto de productos
    producto_d = Producto.objects.filter(id__in=producto_ids_1)
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
        return redirect('carrito')
    
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
    return redirect('carrito') #minuto 4:37 segunda parte del video

def eliminar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('carrito')

def restar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect('carrito')

def limpiar_carrito(request):
    carrito = CarritoClass(request)
    carrito.limpiar()
    return redirect('carrito') 

<<<<<<< HEAD
# def miCarrito(request):
#     return render(request, 'miCarrito.html') 

def miCarrito(request):
    carrito = CarritoClass(request)  # Instancia de la clase Carrito
    return render(request, 'miCarrito.html', {'carrito': carrito.carrito})  # Pasar carrito al template


=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
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
<<<<<<< HEAD
        form = RegistroForm(request.POST) # Mediante esta linea de codigo se obtiene la info del formulario
        if form.is_valid():
            user = form.save(commit=False) # Si el formulario es valido, se crea un objeto en memoria de tipo usuario, pero no lo guarda en la base de datos
            user.set_password(form.cleaned_data['password']) # Se cifra la contraseña para mayor seguridad
            user.save() # Se guarda el usuario en la base de datos
            login(request, user) # Se inicia la sesion del usuario
            return redirect('home') # Re direcciona al home
    else:
        form = RegistroForm()
    return render(request, 'crear_cuenta.html', {'form': form}) # Si el metodo de solicitud no es POST, se genera un formulario vacio

def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) # Si el metodo es POST se obtiene la info del formulario
        if form.is_valid():
            email = form.cleaned_data['email'] 
            password = form.cleaned_data['password'] # Si el formulario es valido se obtiene el correo y la contraseña del usuario
            user = authenticate(request, username=email, password=password) # se verifica si las credenciales son correctas 
            if user is not None:
                login(request, user) # Si las credenciales son validas, se inicia sesion y lo redirige al home
                return redirect('home')
            else:
                messages.error(request, 'Email o contraseña incorrectos') # si las credenciales no son validas se envia un mensaje de error
    else:
        form = LoginForm()
    return render(request, 'inicio_sesion.html', {'form': form}) # Si el metodo de solicitud no es POST, se genera un formulario vacio

def cerrar_sesion(request):
    logout(request) # Cierra la sesion del usuario
=======
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
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
    return redirect('home')

def recuperar(request):
    return render(request, 'recuperar.html')


def perfil(request):
    return render(request, 'perfil_usuario.html')

<<<<<<< HEAD



=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
# def generar_buy_order():
#     return str(uuid.uuid4())

# def generar_session_id():
#     return str(uuid.uuid4())

<<<<<<< HEAD
#____________________________________________________________

def mostrar_carrito(request):
    carrito = CarritoClass(request)
    # Agregar el precio unitario calculado al carrito
    for item in carrito.carrito.values():
        item['precio_unitario'] = item['acumulado'] / item['cantidad'] if item['cantidad'] > 0 else 0

    contexto = {
        'carrito': carrito.carrito
    }
    return render(request, 'miCarrito.html', contexto)
=======
#____________________________________________________________
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
