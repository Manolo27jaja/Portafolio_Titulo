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
from ecommerse.models import Producto, Carrito, CarritoItem, Usuario ,ListaDeseados, Orden, DetalleOrden
from .models import Usuario
from django.db.models import Q # esto es para buscar en django mas especifico dicen 
import mercadopago
from django.conf import settings
import logging
from django.shortcuts import render
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from .models import Carrito, Orden, DetalleOrden
from django.utils.timezone import now
from django.db.models import Sum
from django.db import transaction
from django.http import HttpResponseServerError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Sum, F
logging.basicConfig(level=logging.INFO)


def pago_celular_bricks(request):
    return render(request, 'pago_celular.html', {
        'mercado_pago_public_key': "TEST-0320cb86-4c8b-417b-b52d-c2b487754ddd"
    })
# @csrf_exempt
# def create_preference(request):
#     sdk = mercadopago.SDK("TEST-1910207374097910-101613-31fb1ea48e3de8c63a41f466e1c817e5-2035864462")
    
#     preference_data = {
#         "items": [
#             {
#                 "title": "Celular de prueba",
#                 "quantity": 1,
#                 "unit_price": 1500  # Precio en CLP
#             }
#         ],
        
#         "back_urls": {
#             "success": "https://localhost:8000/pago-exitoso/",
#             "failure": "https://tusitio.com/pago-fallido/",
#         },
#         "auto_return": "approved"
#     }
    
#     preference = sdk.preference().create(preference_data)
#     response = preference.get("response", {})
#     preference_id = response.get("id", None)
    
#     return JsonResponse({"preference_id": preference_id}) if preference_id else JsonResponse({"error": "Error al crear la preferencia"}, status=400)

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
    # Obtener todas las órdenes realizadas por el usuario
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-creado')

    # Calcular el total para cada orden usando F() para multiplicar los campos
    for orden in ordenes:
        orden.total = orden.detalleorden_set.aggregate(
            total=Sum(F('cantidad') * F('precio'))
        )['total'] or 0  # Si no hay detalles, el total será 0

    context = {
        'ordenes': ordenes,
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

@login_required
def mi_carrito(request):
    # Obtener todos los carritos no comprados del usuario
    carritos = Carrito.objects.filter(usuario=request.user, comprado=False).order_by('-creado')

    # Inicializar valores
    items = []  # Lista para los ítems a enviar a Mercado Pago
    total_general = 0  # Total combinado de todos los carritos

    for carrito in carritos:
        for item in carrito.items.all():
            # Sumar el subtotal de cada ítem al total general
            total_general += item.subtotal
            # Agregar los productos al array de Mercado Pago
            items.append({
                "title": item.producto.nombre,
                "quantity": item.cantidad,
                "unit_price": float(item.precio),
                "currency_id": "CLP"  # Asegúrate de usar la moneda correcta
            })

    # Inicializar el SDK de Mercado Pago
    sdk = mercadopago.SDK("TEST-1910207374097910-101613-31fb1ea48e3de8c63a41f466e1c817e5-2035864462")

    # Crear una preferencia única
    if items:
        preference_data = {
            "items": items,
            "back_urls": {
                "success": "https://localhost:8000/pago-exitoso/",
                "failure": "http://127.0.0.1:8000/pago-fallido/",
                "pending": "http://127.0.0.1:8000/pago_pendiente/",
            },
            "auto_return": "approved",
        }
        preference_response = sdk.preference().create(preference_data)
        preference_id = preference_response["response"]["id"]
    else:
        preference_id = None  # No hay ítems, no se genera preferencia

    return render(request, 'miCarrito.html', {
        'carritos': carritos,
        'total_general': total_general,
        'preference_id': preference_id,
    })
# @login_required
# def pago_exitoso(request):
#     print("Vista `pago_exitoso` fue llamada")
#     return render(request,'pago_exitoso.html')

@login_required
def pago_exitoso(request):
    print("Vista `pago_exitoso` fue llamada")
    try:
        # Obtener los carritos no comprados del usuario
        carritos = Carrito.objects.filter(usuario=request.user, comprado=False)

        if not carritos.exists():
            print("No se encontraron carritos activos")
            return render(request, 'pago_fallido.html', {"error": "No se encontró un carrito activo."})

        # Crear la orden
        print("Creando orden")
        orden = Orden.objects.create(
            usuario=request.user,
            creado=now()
        )

        # Crear los detalles de la orden y actualizar el stock
        for carrito in carritos:
            for item in carrito.items.all():
                # Crear un detalle de orden
                DetalleOrden.objects.create(
                    orden=orden,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio=item.precio,
                )
                
                # Actualizar el stock del producto
                producto = item.producto
                if producto.stock >= item.cantidad:
                    producto.stock -= item.cantidad
                    producto.save()
                else:
                    print(f"Stock insuficiente para el producto {producto.nombre}")
                    return render(request, 'pago_fallido.html', {"error": f"Stock insuficiente para el producto {producto.nombre}"})

            # Eliminar el carrito después de guardar los detalles
            carrito.delete()

        # Calcular el total
        total_orden = sum(
            detalle.cantidad * detalle.precio for detalle in orden.detalleorden_set.all()
        )
        print(f"Total de la orden: {total_orden}")

        # Generar el cuerpo del correo
        detalles_orden = "\n".join(
            [
                f"{detalle.cantidad} x {detalle.producto.nombre} - ${detalle.cantidad * detalle.precio:,.2f}"
                for detalle in orden.detalleorden_set.all()
            ]
        )

        mensaje_correo = f"""
Orden Confirmada
¡Gracias por tu compra!

Tu número de orden es: {orden.id}
Fecha: {orden.creado.strftime('%d de %B de %Y a las %H:%M')}
Total: ${total_orden:,.2f}

Detalles de tu orden:
{detalles_orden}

¡Gracias por comprar con nosotros!
"""

        # Enviar correo al usuario
        send_mail(
            subject="¡Tu orden ha sido procesada exitosamente!",
            message=mensaje_correo,
            from_email="tu_correo@tudominio.com",  # Cambia esto por tu dirección de correo
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        print("Correo enviado con éxito")

        # Redirigir al template de pago exitoso con el número de orden y detalles
        return render(request, 'pago_exitoso.html', {
            "orden": orden,
            "detalles": orden.detalleorden_set.all(),
            "total_orden": total_orden,
        })

    except Exception as e:
        print(f"Error en la vista pago_exitoso: {e}")
        return JsonResponse({"error": str(e)}, status=500)

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

from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@login_required
@require_POST
def aumentar_producto_carrito(request, producto_id):
    # Buscar el carrito relacionado con el producto
    carrito = Carrito.objects.filter(usuario=request.user, comprado=False, items__producto_id=producto_id).first()
    
    if carrito:
        # Buscar el item correspondiente al producto en el carrito
        item = carrito.items.filter(producto_id=producto_id).first()
        if item:
            # Aumentar la cantidad
            item.cantidad += 1
            item.save()
    else:
        # Si no hay un carrito asociado, crea uno nuevo
        carrito = Carrito.objects.create(usuario=request.user)
        producto = Producto.objects.get(id=producto_id)
        CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=1, precio=producto.precio)
    
    # Redirigir al carrito para reflejar los cambios
    return redirect('miCarrito')
    # Redirigir al carrito para reflejar los cambios
    return redirect('miCarrito')  # Corrige aquí cualquier mezcla de espacios/tabulaciones

@login_required
@require_POST
def disminuir_producto_carrito(request, producto_id):
    # Buscar el carrito relacionado con el producto
    carrito = Carrito.objects.filter(usuario=request.user, comprado=False, items__producto_id=producto_id).first()
    
    if carrito:
        # Buscar el item correspondiente al producto en el carrito
        item = carrito.items.filter(producto_id=producto_id).first()
        if item:
            # Disminuir la cantidad, pero no permitir que sea menor a 1
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
            else:
                # Si la cantidad es 1, eliminar el producto
                item.delete()

                # Verificar si el carrito está vacío y eliminarlo si es necesario
                if not carrito.items.exists():
                    carrito.delete()
    
    # Redirigir al carrito para reflejar los cambios
    return redirect('miCarrito')

@login_required
@require_POST
def eliminar_producto_carrito(request, producto_id):
    # Obtener el carrito relacionado con el producto
    carrito = Carrito.objects.filter(usuario=request.user, comprado=False, items__producto_id=producto_id).first()
    
    if carrito:
        # Obtener el item correspondiente al producto en el carrito
        item = carrito.items.filter(producto_id=producto_id).first()
        if item:
            # Eliminar el producto
            item.delete()
            
            # Verificar si el carrito está vacío
            if not carrito.items.exists():
                # Si está vacío, eliminar el carrito
                carrito.delete()
    
    # Redirigir al carrito después de eliminar el producto y el carrito si es necesario
    return redirect('miCarrito')

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
@require_POST
def actualizar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    nuevo_stock = request.POST.get('stock')
    if nuevo_stock.isdigit():
        producto.stock = int(nuevo_stock)
        producto.save()
    return redirect('dashboard_admin')

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