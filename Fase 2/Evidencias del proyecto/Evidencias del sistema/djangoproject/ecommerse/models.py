# Abstract es para usar los campos creados en la base de datos por el desarrollador y no por django
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Importa la libreria de dijango para hacer modelos de base de datos
from django.db import models
from django.conf import settings

# Aqui se crea la base de datos
# Crea la base de datos del carrito de compras, una base de datos basica para hacer funcionar funcionalidades.
# Tabla producto
class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=32)
    precio = models.IntegerField()
    imagen = models.ImageField()
    descripcion = models.CharField(max_length=255, default='Descripción por defecto')
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=10)
    memoria_ram = models.CharField(max_length=20 , default='2 ram') 
    sistema_operativo = models.CharField(max_length=50,default='Windows')
    tamaño_pantalla = models.CharField(max_length=30, default='1470 x 2010')
    procesador = models.CharField(max_length=100, default='Sin descripción')
    tarjeta_grafica = models.CharField(max_length=50, default='Si')
    descripcion_tg = models.CharField(max_length=200, default='tarjeta amd alta gama')

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

    # def __str__(self):
    #     return self.nombre
    
    def es_stock_bajo(self):
        return self.stock_actual <= self.stock_minimo


#________________________________________________________        

#___________________________________
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

    def create_superuser(self, email, nombre, password, telefono): # Metodo para crear el super usuario, con los campos especificados
        user = self.create_user(email, nombre, password, telefono) # Se pasan los argumentos al create_user, devolviendo un objeto de tipo usuario 
        user.is_staff = True
        user.is_superuser = True # Se le asignan las propiedades de un super usuario
        user.save(using=self._db) # Lo guarda en la base de datos
        return user

class Usuario(AbstractBaseUser, PermissionsMixin): # Definimos un modelo personalizado para nuesto usuario/ AbstractBaseUser nos proporciona la insfraestructura basica para un usuario personalizado/Añade soperte para el sistema de permisos de django
    email = models.EmailField(unique=True) # Correo unico
    nombre = models.CharField(max_length=30) 
    telefono = models.CharField(max_length=15, blank=False, null=True) # El telefono puede ser nullo o blank
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # por default es false a menos que se cree como super usuario por medio de comandos
    is_superuser = models.BooleanField(default=False) # por default es false a menos que se cree como super usuario por medio de comandos

    objects = UsuarioManager() # Asignamos UsuarioManager como administrador del modelo, lo que nos permite utilizar los metodos de este para crear usuarios

    USERNAME_FIELD = 'email' # Se define el email como identificador principal
    REQUIRED_FIELDS = ['nombre','telefono'] # Se define que los campos adicionales son obligatorios (para el super usuario)

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        """Verifica si el usuario tiene un permiso específico."""
        return self.is_superuser  # verifica si el usuario tiene permisos

    def has_module_perms(self, app_label):
        """Verifica si el usuario tiene permisos para ver una app específica."""
        return self.is_superuser  # Los superusuarios pueden ver todas las apps
#_____________________________________________
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el modelo de Usuario
    creado = models.DateTimeField(auto_now_add=True)  # Fecha de creación del carrito
    comprado = models.BooleanField(default=False)

    def calcular_total(self):
        total = 0
        for item in self.items.all():
            total += item.cantidad * item.precio
        return total

    def __str__(self):
        return f'Carrito de {self.usuario.email}'
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')  # Relación con el carrito
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)  # Relación con el producto
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} en el carrito de {self.carrito.usuario.email}'    
#_______________________________________________
    


# para los deseados
class ListaDeseados(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'producto')


class Almacenamiento(models.Model):
    capacidad = models.CharField(max_length=16)  # Ejemplo: "128GB", "256GB"

    def __str__(self):
        return self.capacidad

class Color(models.Model):
    nombre = models.CharField(max_length=32)
    codigo_hex = models.CharField(max_length=7, null=True, blank=True)  # Opcional: código HEX para representar el color

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=64)

    def __str__(self):
        return self.nombre
    
#_________________________
    
class ProductoAlmacenamiento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    almacenamiento = models.ForeignKey(Almacenamiento, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'almacenamiento')  # Asegura combinaciones únicas

class ProductoColor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'color')

class ProductoModelo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto','modelo')

    # class Meta:
    #     unique_together = ('producto', 'modelo')