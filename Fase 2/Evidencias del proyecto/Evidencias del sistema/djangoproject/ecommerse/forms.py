from django import forms # Se importa el modulo de formularios de django, permite crear formularios personalizados
from .models import Usuario # Se importa el modelo Usuario, este modelo representa al usuario en la base de datos
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import SetPasswordForm
from .models import Producto, ProductoModelo


from django import forms
from .models import Usuario  # Asegúrate de que este es tu modelo personalizado de usuario

class RegistroForm(forms.ModelForm):
    # Campos personalizados
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        label="Contraseña"
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar contraseña"
    )

    class Meta:
        model = Usuario  # Define el modelo asociado
        fields = ['nombre', 'email', 'telefono', 'password']  # Lista de campos a incluir en el formulario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """Validación personalizada para verificar que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password and confirmar_password and password != confirmar_password:
            self.add_error('confirmar_password', "Las contraseñas no coinciden.")

        return cleaned_data

    class Meta: # Es una clase interna que define las configuraciones para el formulario.
        model = Usuario # Se especifica el modelo que se usara
        fields = ['nombre', 'email', 'telefono', 'password'] # Se especifican los campos que se usaran
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

    def clean_confirmar_password(self): # Metodo para validar que los campos de contraseña y confirmar contraseña coincidan
        password = self.cleaned_data.get('password')
        confirmar_password = self.cleaned_data.get('confirmar_password')

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return confirmar_password


    def clean_password(self): # Metodo la validar que la contraseña es correcta
        password = self.cleaned_data.get('password') # Obtiene la contraseña ingresada por el usuario

    # Verificar si la contraseña tiene al menos 8 caracteres
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")

    # Verificar si la contraseña contiene al menos una letra mayúscula
        if not any(char.isupper() for char in password):
            raise ValidationError("La contraseña debe tener al menos una letra mayúscula")

    # Verificar si la contraseña contiene al menos un número
        if not any(char.isdigit() for char in password):
            raise ValidationError("La contraseña debe tener al menos un número")

    # Verificar si la contraseña contiene al menos un carácter especial
        if not any(char in '!@#$%^&*()_+[]{}|;:,.<>?/~`-=' for char in password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial como !@#$%^&*()")
            
        return password

    def clean_telefono(self): # Metodo para que solamnte se ingresen numeros en el input de numero de telefono
        telefono = self.cleaned_data.get('telefono')
    # Validar si el número de teléfono tiene el formato correcto (solo números)
        if not re.match(r'^\d{9}$', telefono):
            raise ValidationError("El número de teléfono debe contener 9 dígitos")
        return telefono


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# class CustomSetPasswordForm(SetPasswordForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['new_password1'].error_messages = {
#             'password_too_similar': 'La nueva contraseña es demasiado similar a tu información personal.',
#             'password_too_short': 'La contraseña debe tener al menos 8 caracteres.',
#             'password_too_common': 'La contraseña es demasiado común.',
#             'password_entirely_numeric': 'La contraseña no puede ser solo numérica.'
#         }



from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'descripcion', 'imagen','stock_actual','memoria_ram','sistema_operativo','tamaño_pantalla','procesador','tarjeta_grafica','descripcion_tg']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'dashboard-input'}),
            'categoria': forms.TextInput(attrs={'class': 'dashboard-input'}),  
            'precio': forms.NumberInput(attrs={'class': 'dashboard-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'dashboard-input dashboard-textarea'}),
            'imagen': forms.FileInput(attrs={'class': 'dashboard-input'}),
            'stock_actual': forms.NumberInput(attrs={'class':'dashboard-input'}),
            'memoria_ram': forms.TextInput(attrs={'class': 'dashboard-input'}),
            'sistema_operativo': forms.TextInput(attrs={'class': 'dashboard-input'}),
            'tamaño_pantalla': forms.TextInput(attrs={'class': 'dashboard-input'}),
            'procesador': forms.TextInput(attrs={'class': 'dashboard-input'}),
            'tarjeta_grafica': forms.TextInput(attrs={'class': 'dashboard-input'}),
            'descripcion_tg': forms.TextInput(attrs={'class': 'dashboard-input'}),
            

        }


class ProductoModeloForm(forms.Form):
    modelo = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'dashboard-input'}),
        required=True
    )

class ProductoColorForm(forms.Form):
    color = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'dashboard-input'}),
        required=True
    )
    codigo_hex = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={'class': 'dashboard-input', 'placeholder': '#RRGGBB'}),
        required=True
    )

class ProductoAlmacenamientoForm(forms.Form):
    capacidad = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'class':'dashboard-input'}),
        required=True
    )




