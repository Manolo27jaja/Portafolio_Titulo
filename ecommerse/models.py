# Importa la librería de Django para hacer modelos de base de datos
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#probando weassss

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

# Aquí se crea la base de datos
# Crea la base de datos del carrito de compras, una base de datos básica para hacer funcionar funcionalidades.

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

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Verifica si el usuario tiene un permiso específico."""
        return self.is_superuser  # Los superusuarios tienen todos los permisos

    def has_module_perms(self, app_label):
        """Verifica si el usuario tiene permisos para ver una app específica."""
        return self.is_superuser  # Los superusuarios pueden ver todas las apps


class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=32)
    precio = models.IntegerField()
    imagen = models.ImageField()
    descripcion = models.CharField(max_length=255, default='Descripción por defecto')

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'

#creee una tabla llamada carrito------------------------------------------------------------------,-,,-,-,-,,
    
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario} - {self.producto} (Cantidad: {self.cantidad})'


@login_required
def agregar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Guardar el producto en el carrito de la base de datos
    carrito_item, created = Carrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not created:
        # Si el producto ya está en el carrito, aumentar la cantidad
        carrito_item.cantidad += 1
        carrito_item.save()

    return redirect('carrito')  # Redirige a la vista del carrito