from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'password']

    def clean_confirmar_password(self):
        password = self.cleaned_data.get('password')
        confirmar_password = self.cleaned_data.get('confirmar_password')

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return confirmar_password


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)