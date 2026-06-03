from django.urls import path

from . import views

urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'),
    path('salas/', views.SalaListaView.as_view(), name='lista_salas'),
    path('salas/<uuid:pk>/', views.SalaDetailView.as_view(), name='detalle_sala'),
    path('salas/nueva/', views.SalaCrearView.as_view(), name='sala_crear_admin'),
    path('salas/<uuid:pk>/editar/', views.SalaEditarView.as_view(), name='sala_editar_admin'),
    path('reservas/', views.ReservaListaView.as_view(), name='lista_reservas'),
    path('reservas/nueva/', views.ReservaCrearView.as_view(), name='reserva_crear'),
    path('reservas/<uuid:pk>/cancelar/', views.ReservaCancelarView.as_view(), name='reserva_cancelar'),
    path('reservas/<uuid:pk>/mover/', views.ReservaMoverView.as_view(), name='reserva_mover'),
    path('calendario/', views.CalendarioView.as_view(), name='calendario'),
]