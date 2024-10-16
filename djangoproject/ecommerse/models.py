# Abstract es para usar los campos creados en la base de datos por el desarrollador y no por django
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Importa la libreria de dijango para hacer modelos de base de datos
from django.db import models

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

#___________________________________
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

    def _str_(self):
        return self.email


    def has_perm(self, perm, obj=None):
        """Verifica si el usuario tiene un permiso específico."""
        return self.is_superuser  # Los superusuarios tienen todos los permisos

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
#_______________________________________________