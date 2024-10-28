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
from .models import Usuario, Carrito , ListaDeseados



def home(request):
    producto_ids_1 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Primer conjunto de productos
    producto_ids_2 = [7, 8, 9, 10, 11, 12]  # Segundo conjunto de productos para el otro carrusel
    producto_ids_3 = [7, 8, 9]  # Tercer conjunto de productos

    productos_1 = Producto.objects.filter(id__in=producto_ids_1)
    productos_2 = Producto.objects.filter(id__in=producto_ids_2)
    productos_3 = Producto.objects.filter(id__in=producto_ids_3)  # Nuevos productos

    por_categorias_1 = Producto.objects.filter(categoria="Consola")[:4]
    por_categorias_2 = Producto.objects.filter(categoria="Computadores")[:4]
    por_categorias_3 = Producto.objects.filter(categoria="Accesorios")[:4]  # Nueva categoría

    return render(request, 'home.html', {
        "productos_1": productos_1,
        "productos_2": productos_2,
        "productos_3": productos_3,  # Añade aquí la nueva sección
        "por_categorias_1": por_categorias_1,
        "por_categorias_2": por_categorias_2,
        "por_categorias_3": por_categorias_3  # Añade aquí la nueva categoría
    })

#_________________________________________________

<<<<<<< HEAD:djangoproject/ecommerse/views.py



def carrito(request):
    producto_ids_1 = [5, 4]  # Primer conjunto de productos
    producto_d = Producto.objects.filter(id__in=producto_ids_1)
    return render(request, 'carrito.html', {"productos": producto_d})

=======
def carritoid(request, producto_id):
    producto_d = Producto.objects.filter(id=producto_id)
    return render(request, 'carrito.html', {"productos":producto_d})
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/ecommerse/views.py

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
<<<<<<< HEAD:djangoproject/ecommerse/views.py
        return redirect('carrito')
=======
        return redirect('home')
    
#_______________________________________________________
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/ecommerse/views.py

#_______________________________________________________

def read_ingreso(request):
    return render(request, 'inicio_sesion.html')

def agregar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
<<<<<<< HEAD:djangoproject/ecommerse/views.py
    return redirect('carrito')
=======
    return redirect('carritoid', producto_id=producto.id) #minuto 4:37 segunda parte del video
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/ecommerse/views.py

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

# Metodos de sistema login
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

<<<<<<< HEAD:djangoproject/ecommerse/views.py
#____________________________________________________________
=======
<<<<<<< HEAD



=======
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4
# def generar_buy_order():
#     return str(uuid.uuid4())
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/ecommerse/views.py


<<<<<<< HEAD:djangoproject/ecommerse/views.py
def mostrar_producto_carrito(request):
    # Obtiene todos los carritos para el usuario
    carritos = Carrito.objects.filter(usuario=request.user)

    if carritos.exists():
        # Si hay carritos, selecciona el primero (puedes personalizar esta lógica)
        carrito = carritos.first()
        items = carrito.items.all()  # Obtiene todos los items del carrito
    else:
        items = []  # No hay items si no existe el carrito

    return render(request, 'producto_carrito.html', {'items': items})







@login_required
def agregar_deseado(request, producto_id):
    print(f"Usuario autenticado: {request.user.is_authenticated}")  # Verifica si el usuario está autenticado
    producto = get_object_or_404(Producto, id=producto_id)
    deseado, created = ListaDeseados.objects.get_or_create(usuario=request.user, producto=producto)

    if created:
        messages.success(request, f'¡Has añadido {producto.nombre} a tus deseados!')
    else:
        messages.info(request, f'{producto.nombre} ya está en tu lista de deseados.')
    
    return redirect('ver_deseados')

@login_required
def eliminar_deseado(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    ListaDeseados.objects.filter(usuario=request.user, producto=producto).delete()
    return redirect('ver_deseados')


@login_required
def ver_deseados(request):
    productos_deseados = ListaDeseados.objects.filter(usuario=request.user).select_related('producto')
    return render(request, 'deseados.html', {'productos_deseados': productos_deseados})

def deseados(request):
    return render(request, 'deseados.html')
=======
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
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/ecommerse/views.py
