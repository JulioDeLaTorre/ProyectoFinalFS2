from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class IniciarSesionForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario o correo',
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'usuario o correo@ejemplo.com'}),
    )


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre_completo = forms.CharField(
        max_length=150,
        required=False,
        label='Nombre completo',
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono',
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'nombre_completo',
            'telefono',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nombre_completo = self.cleaned_data.get('nombre_completo') or ''
        user.telefono = self.cleaned_data.get('telefono') or None
        if commit:
            user.save()
        return user
