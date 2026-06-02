from django.urls import path

from . import views

urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'),
    path('salas/', views.SalaListaView.as_view(), name='lista_salas'),
    path('reservas/', views.ReservaListaView.as_view(), name='lista_reservas'),
    path('reservas/nueva/', views.ReservaCrearView.as_view(), name='reserva_crear'),
    path('calendario/', views.CalendarioView.as_view(), name='calendario'),
]
