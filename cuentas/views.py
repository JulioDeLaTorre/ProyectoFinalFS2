from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import IniciarSesionForm, RegistroForm
from .models import CustomUser


class IniciarSesionView(LoginView):
    template_name = 'cuentas/login.html'
    redirect_authenticated_user = True
    authentication_form = IniciarSesionForm


class CerrarSesionView(LogoutView):
    pass


class RegistroView(CreateView):
    model = CustomUser
    form_class = RegistroForm
    template_name = 'cuentas/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Cuenta creada. Ya puedes iniciar sesión.',
        )
        return super().form_valid(form)


class CambiarContrasenaView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'cuentas/cambiar_contrasena.html'
    success_url = reverse_lazy('cambiar_contrasena_hecho')


class CambiarContrasenaHechoView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'cuentas/cambiar_contrasena_hecho.html'


class RestablecerContrasenaView(PasswordResetView):
    template_name = 'cuentas/restablecer_contrasena.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class RestablecerContrasenaHechoView(PasswordResetDoneView):
    template_name = 'cuentas/restablecer_contrasena_hecho.html'


class RestablecerContrasenaConfirmarView(PasswordResetConfirmView):
    template_name = 'cuentas/restablecer_contrasena_confirmar.html'
    success_url = reverse_lazy('password_reset_complete')


class RestablecerContrasenaCompletoView(PasswordResetCompleteView):
    template_name = 'cuentas/restablecer_contrasena_completo.html'


class MiCuentaView(LoginRequiredMixin, TemplateView):
    template_name = 'cuentas/mi_cuenta.html'
