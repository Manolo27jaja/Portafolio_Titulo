# Abstract es para usar los campos creados en la base de datos por el desarrollador y no por django
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings  # Importa settings

# Importa la libreria de dijango para hacer modelos de base de datos
from django.db import models
from django.utils import timezone 
from django.shortcuts import render


# Aqui se crea la base de datos
# Crea la base de datos del carrito de compras, una base de datos basica para hacer funcionar funcionalidades.

# Tabla producto
class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=32)
    precio = models.IntegerField()
    imagen = models.ImageField()
    descripcion = models.CharField(max_length=255, default='Descripción por defecto')

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

#________________________________________________________        

<<<<<<< HEAD:djangoproject/ecommerse/models.py

=======
#___________________________________
<<<<<<< HEAD
class UsuarioManager(BaseUserManager): # Administracion personalizado para el modelo usuario, permite crear usuarios y superusuarios de manera mas sensilla
    def create_user(self, email, nombre, password, telefono): # El metodo crea un nuevo usuario con los 4 campos obligatorios
        if not email:
            raise ValueError('El email es obligatorio')
        if not password:
            raise ValueError('La contraseña es obligatoria')
        if not telefono:
            raise ValueError('El teléfono es obligatorio')
        if not nombre:
            raise ValueError('El nombre es obligatorio')
        email = self.normalize_email(email) # El correo es normalizado, convirtiendo en minusculas y eliminando cualquier espacio no deseado
        user = self.model(email=email, nombre=nombre, telefono=telefono) # Crea una instacia del modelo usuario, sin guardar nada en la base de datos
        user.set_password(password) # Se encripta la contraseña para guardarla en la base de datos
        user.save(using=self._db) # Guarda el usuario en la base de datos
        return user

    def create_superuser(self, email, nombre, password): # Metodo para crear el super usuario, con los campos especificados
        user = self.create_user(email, nombre, password) # Se pasan los argumentos al create_user, devolviendo un objeto de tipo usuario 
        user.is_staff = True
        user.is_superuser = True # Se le asignan las propiedades de un super usuario
        user.save(using=self._db) # Lo guarda en la base de datos
        return user

class Usuario(AbstractBaseUser, PermissionsMixin): # Definimos un modelo personalizado para nuesto usuario/ AbstractBaseUser nos proporciona la insfraestructura basica para un usuario personalizado/Añade soperte para el sistema de permisos de django
    email = models.EmailField(unique=True) # Correo unico
    nombre = models.CharField(max_length=30) 
    telefono = models.CharField(max_length=15, blank=False, null=False) # El telefono puede ser nullo o blank
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # por default es false a menos que se cree como super usuario por medio de comandos
    is_superuser = models.BooleanField(default=False) # por default es false a menos que se cree como super usuario por medio de comandos

    objects = UsuarioManager() # Asignamos UsuarioManager como administrador del modelo, lo que nos permite utilizar los metodos de este para crear usuarios

    USERNAME_FIELD = 'email' # Se define el email como identificador principal
    REQUIRED_FIELDS = ['nombre','telefono'] # Se define que los campos adicionales son obligatorios (para el super usuario)
=======
>>>>>>> 72e7c0c2bc4e0a695a307a2a0a61796b08eb308a:Fase 2/Evidencias del proyecto/Evidencias del sistema/djangoproject/ecommerse/models.py
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None, telefono=None):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, telefono=telefono)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None):
        user = self.create_user(email, nombre, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db) 
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, default='example@example.com')
    nombre = models.CharField(max_length=30, default='Usuario')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Verifica si el usuario tiene un permiso específico."""
<<<<<<< HEAD
        return self.is_superuser  # verifica si el usuario tiene permisos
=======
        return self.is_superuser  # Los superusuarios tienen todos los permisos
>>>>>>> 02e8b3697dcc47d645419c7bd46c834e358461b4

    def has_module_perms(self, app_label):
        """Verifica si el usuario tiene permisos para ver una app específica."""
        return self.is_superuser  # Los superusuarios pueden ver todas las apps

#_____________________________________________

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el modelo de Usuario
    creado = models.DateTimeField(auto_now_add=True)  # Fecha de creación del carrito
    

    def __str__(self):
        return f'Carrito de {self.usuario.email}'

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')  # Relación con el carrito
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)  # Relación con el producto
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en el carrito de {self.carrito.usuario.email}'

#_______________________________________________________________
    

    
class ListaDeseados(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'producto')  # Para evitar duplicado


        

def mostrar_detalles_compra(request):
    # Obtiene los productos del carrito
    carritos = Carrito.objects.filter(usuario=request.user)
    items = []

    if carritos.exists():
        carrito = carritos.first()
        items = carrito.items.all()

    # Establece un tiempo estimado de envío (puedes modificarlo según tu lógica)
    tiempo_envio = "3-5 días hábiles"  # Esto es solo un ejemplo

    return render(request, 'producto_carrito.html', {'items': items, 'tiempo_envio': tiempo_envio})





class ListaDeseados(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'producto')  # Para evitar duplicado