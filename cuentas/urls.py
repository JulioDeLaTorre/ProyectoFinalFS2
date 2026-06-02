from django.urls import path

from . import views

urlpatterns = [
    path('cuentas/registro/', views.RegistroView.as_view(), name='registro'),
    path('cuentas/login/', views.IniciarSesionView.as_view(), name='login'),
    path('cuentas/logout/', views.CerrarSesionView.as_view(), name='logout'),
    path('cuentas/mi-cuenta/', views.MiCuentaView.as_view(), name='mi_cuenta'),
    path(
        'cuentas/cambiar-contrasena/',
        views.CambiarContrasenaView.as_view(),
        name='cambiar_contrasena',
    ),
    path(
        'cuentas/cambiar-contrasena/hecho/',
        views.CambiarContrasenaHechoView.as_view(),
        name='cambiar_contrasena_hecho',
    ),
    path(
        'cuentas/restablecer-contrasena/',
        views.RestablecerContrasenaView.as_view(),
        name='password_reset',
    ),
    path(
        'cuentas/restablecer-contrasena/enviado/',
        views.RestablecerContrasenaHechoView.as_view(),
        name='password_reset_done',
    ),
    path(
        'cuentas/restablecer-contrasena/<uidb64>/<token>/',
        views.RestablecerContrasenaConfirmarView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'cuentas/restablecer-contrasena/completo/',
        views.RestablecerContrasenaCompletoView.as_view(),
        name='password_reset_complete',
    ),
]
