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
from ecommerse.models import Producto, Carrito, CarritoItem, Usuario ,ListaDeseados
from .models import Usuario
from django.http import JsonResponse

from django.db.models import Q # esto es para buscar en django mas especifico dicen 
import mercadopago
from django.conf import settings
import logging
from django.shortcuts import render
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

logging.basicConfig(level=logging.INFO)

def pago_celular_bricks(request):
    return render(request, 'pago_celular.html', {
        'mercado_pago_public_key': "TEST-0320cb86-4c8b-417b-b52d-c2b487754ddd"
    })
@csrf_exempt
def create_preference(request):
    sdk = mercadopago.SDK("TEST-1910207374097910-101613-31fb1ea48e3de8c63a41f466e1c817e5-2035864462")
    
    preference_data = {
        "items": [
            {
                "title": "Celular de prueba",
                "quantity": 1,
                "unit_price": 1500  # Precio en CLP
            }
        ],
        
        "back_urls": {
            "success": "https://tusitio.com/pago-exitoso/",
            "failure": "https://tusitio.com/pago-fallido/",
        },
        "auto_return": "approved"
    }
    
    preference = sdk.preference().create(preference_data)
    response = preference.get("response", {})
    preference_id = response.get("id", None)
    
    return JsonResponse({"preference_id": preference_id}) if preference_id else JsonResponse({"error": "Error al crear la preferencia"}, status=400)

def pagar(request):
    return render(request, 'pago_celular.html')



def modal(request):
    return render(request, 'modal.html')

def contenido_carrito(request, producto_id):
    return render(request, 'contenido_carrito.html')

def detalle_producto(request, producto_id):
    d_p_real = Producto.objects.filter(id=producto_id)
    producto_ids_1 = [1, 2, 3, 4, 5, 6, 7, 8] 
    productos_1 = Producto.objects.filter(id__in=producto_ids_1)
    return render(request, 'detalle_producto.html', {"d_p_real": d_p_real, "productos_1": productos_1})

def home(request):
    producto_ids_1 = [1, 2, 3, 4, 5, 6]  # Primer conjunto de productos
    producto_ids_2 = [7, 8, 9, 10, 11, 12]  # Segundo conjunto de productos para el otro carrusel
    productos_1 = Producto.objects.filter(id__in=producto_ids_1)
    productos_2 = Producto.objects.filter(id__in=producto_ids_2)
    por_categorias_1 = Producto.objects.filter(categoria="Consola")[:4]
    por_categorias_2 = Producto.objects.filter(categoria="Computadores")[:4]
    return render(request, 'home.html', {"productos_1": productos_1, "productos_2": productos_2, "por_categorias_1": por_categorias_1, "por_categorias_2": por_categorias_2})
#_________________________________________________



@login_required
def mis_compras(request):
    # Carritos no comprados (pedidos)
    pedidos = Carrito.objects.filter(usuario=request.user, comprado=False)
    # Carritos comprados
    compras = Carrito.objects.filter(usuario=request.user, comprado=True)

    # Calcula el total para cada carrito
    for carrito in pedidos:
        carrito.total = carrito.calcular_total()
    for carrito in compras:
        carrito.total = carrito.calcular_total()

    context = {
        'pedidos': pedidos,
        'compras': compras
    }   
    return render(request, 'mis_compras.html', context)

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
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    html_carrito = render_to_string('detalle_producto.html', {'carrito': carrito})

    return JsonResponse({
        "status": "Producto agregado al carrito",
        "producto_id": producto.id,
        "nueva_cantidad": carrito.obtener_cantidad(producto),
        "html": html_carrito  # HTML del carrito para actualizar el modal
    })
    
def aumentar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)  # Se asume que `agregar` también aumenta la cantidad si el producto ya está en el carrito
    return JsonResponse({
        "status": "Cantidad actualizada",
        "producto_id": producto.id,
        "nueva_cantidad": carrito.obtener_cantidad(producto)#,  # Llamada al nuevo método para obtener la cantidad
        #"total_carrito": carrito.obtener_total()  # Total actualizado
    })

def eliminar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('carritoid', producto_id=producto.id)

def restar_producto(request, producto_id):
    carrito = CarritoClass(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return JsonResponse({
        "status": "Cantidad actualizada",
        "producto_id": producto.id,
        "nueva_cantidad": carrito.obtener_cantidad(producto)#,  # Método que devuelve la nueva cantidad
        #"total_carrito": carrito.obtener_total()  # Método que devuelve el total del carrito
    })

def limpiar_carrito(request):
    carrito = CarritoClass(request)
    carrito.limpiar()
    return redirect('carritoid')

# def miCarrito(request):
#     return render(request, 'miCarrito.html') 

def miCarrito(request):
    carrito = CarritoClass(request)  # Instancia de la clase Carrito
    return render(request, 'miCarrito.html', {'carrito': carrito.carrito})  # Pasar carrito al template
#_____________________________________________________


#_______________buscar corregido______________________________________

def buscar(request):
    query = request.GET.get('q', '')  
    if query:
        resultados = Producto.objects.filter(Q(nombre__icontains=query) | Q(categoria__icontains=query))
    else:
        resultados = Producto.objects.none()
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

def mostrar_carrito(request):
    carrito = CarritoClass(request)
    # Agregar el precio unitario calculado al carrito
    for item in carrito.carrito.values():
        item['precio_unitario'] = item['acumulado'] / item['cantidad'] if item['cantidad'] > 0 else 0

    contexto = {
        'carrito': carrito.carrito
    }
    return render(request, 'miCarrito.html', contexto)

#__________MIS DESEADOS________________________________________

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
def eliminar_deseado(request, deseado_id):
    # Busca el objeto ListaDeseados por su ID
    deseado = get_object_or_404(ListaDeseados, id=deseado_id, usuario=request.user)
    deseado.delete()
    messages.success(request, '¡Producto eliminado de la lista de deseados!')
    return redirect('ver_deseados')



@login_required
def ver_deseados(request):
    productos_deseados = ListaDeseados.objects.filter(usuario=request.user).select_related('producto')
    return render(request, 'deseados.html', {'productos_deseados': productos_deseados})

def deseados(request):
    return render(request, 'deseados.html')


#-----------------------------------------------

#------------PARA HACER INGRESO DE PRODUCTOS AL DASHBOARD----------------------------

from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Producto
from .forms import ProductoForm

# Decorador para permitir solo a administradores
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@admin_required
def dashboard_admin(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Extraer los datos del formulario
            nombre = form.cleaned_data['nombre']
            categoria = form.cleaned_data['categoria']
            precio = form.cleaned_data['precio']
            imagen = form.cleaned_data['imagen']
            descripcion = form.cleaned_data['descripcion']
            
            # Llamar al procedimiento almacenado
            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL InsertarProducto(%s, %s, %s, %s, %s)", 
                    [nombre, categoria, precio, imagen.name, descripcion]
                )
            
            messages.success(request, '¡Producto agregado exitosamente!')
            return redirect('dashboard_admin')
    else:
        form = ProductoForm()
    
    productos = Producto.objects.all()  # Para mostrar los productos en el dashboard
    context = {
        'form': form,
        'productos': productos
    }
    return render(request, 'dashboard_admin.html', context)



def editar_producto(request, producto_id):
    # Obtén el producto a editar
    producto = get_object_or_404(Producto, id=producto_id)

    # Si el formulario fue enviado con el método POST
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()  # Guarda los cambios
            messages.success(request, "¡Producto actualizado con éxito!")  
            return redirect('dashboard_admin')  
    else:
        form = ProductoForm(instance=producto)  

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})





@admin_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        producto.delete()  # Elimina el producto
        messages.success(request, "Producto eliminado con éxito.")  
        return redirect('dashboard_admin') 
    
    context = {
        'producto': producto
    }
    return render(request, 'eliminar_producto.html', context)




#------------PARA HACER DASHBOARD GRAFICO----------------------------

from django.shortcuts import render
from django.db.models import Sum
from .models import Producto, CarritoItem

def dashboard_graficos(request):
    # Obtenemos el total vendido por categoría
    ventas_por_categoria = CarritoItem.objects.values('producto__categoria') \
        .annotate(total_vendido=Sum('cantidad')) \
        .order_by('-total_vendido')

    print(ventas_por_categoria)  

    # Pasamos los datos al template
    return render(request, 'dashboard_graficos.html', {'ventas_por_categoria': ventas_por_categoria})