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
import mercadopago
from django.conf import settings
import logging
from django.shortcuts import render
from django.contrib.auth import logout

logging.basicConfig(level=logging.INFO)

def pago_celular_bricks(request):
    # Crear una instancia del SDK de Mercado Pago usando el Access Token
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    # Definir los datos de la preferencia
    preference_data = {
        "items": [
            {
                "title": "Celular",
                "quantity": 1,
                "currency_id": "CLP",
                "unit_price": 1500.00
            }
        ],
        "payer": {
            "email": "comprador@ejemplo.com"  # Asegúrate de usar un correo de prueba
        },
        "back_urls": {
            "success": "http://localhost:8000/pago-exitoso/",
            "failure": "http://localhost:8000/pago-fallido/"
        },
        "auto_return": "approved",
        "payment_methods": {
            "excluded_payment_types": [],  # Asegúrate de no excluir métodos si no es necesario
            "installments": 12  # Máximo de 12 cuotas
        },
        "notification_url": "http://localhost:8000/notificaciones/",
    }

    # Intentar crear la preferencia y capturar la respuesta de la API
    try:
        preference = sdk.preference().create(preference_data)

        # Capturar la respuesta de la API
        response = preference.get('response', {})
        status = preference.get('status', 'error')
        
        # Log para depuración
        logging.info(f"Mercado Pago API Response: {response}")

        # Comprobar si se creó la preferencia correctamente
        if status == 201:  # Status 201 indica éxito en la creación de la preferencia
            context = {
                'preference_id': response.get('id'),
                'mercado_pago_public_key': settings.MERCADOPAGO_PUBLIC_KEY,
                'sandbox_init_point': response.get('sandbox_init_point')  # Utilizar sandbox URL si es necesario
            }
            return render(request, 'pago_celular_bricks.html', context)
        else:
            # Si ocurre un error, mostrar el mensaje de error
            logging.error(f"Error en la creación de la preferencia: {response}")
            return JsonResponse({'error': 'No se pudo crear la preferencia', 'response': response}, status=400)
    
    except Exception as e:
        logging.error(f"Error en la creación de la preferencia: {e}")
        return JsonResponse({'error': 'Ocurrió un error en el servidor', 'details': str(e)}, status=500)

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

def pago_exitoso(request):
    """Vista para manejar pagos exitosos."""
    return render(request, 'pago_exitoso.html')

def pago_fallido(request):
    """Vista para manejar pagos fallidos."""
    return render(request, 'pago_fallido.html')

# def generar_buy_order():
#     return str(uuid.uuid4())

# def generar_session_id():
#     return str(uuid.uuid4())

#____________________________________________________________