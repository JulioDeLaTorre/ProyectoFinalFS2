from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Reserva, Sala

class InicioView(TemplateView):
    template_name = 'inicio.html'


class SalaListaView(ListView):
    model = Sala
    template_name = 'reservas/sala_lista.html'
    context_object_name = 'salas'
    paginate_by = 12

    def get_queryset(self):
        # AQUI AGREGAMOS EL ORDER_BY PARA QUITAR EL WARNING
        qs = super().get_queryset().order_by('nombre')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(ubicacion__icontains=q))
        return qs


class SalaDetailView(DetailView):
    model = Sala
    template_name = 'reservas/sala_detail.html'
    context_object_name = 'sala'

class SalaCrearView(UserPassesTestMixin, CreateView):
    model = Sala
    template_name = 'reservas/sala_form.html'
    fields = [
        'nombre', 'descripcion', 'ubicacion', 'capacidad_maxima', 
        'precio_por_hora', 'precio_por_dia', 'estado', 'tipo_plano', 'imagen_portada'
    ]
    success_url = reverse_lazy('lista_salas')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
class SalaEditarView(UserPassesTestMixin, UpdateView):
    model = Sala
    template_name = 'reservas/sala_form.html'
    fields = [
        'nombre', 'descripcion', 'ubicacion', 'capacidad_maxima', 
        'precio_por_hora', 'precio_por_dia', 'estado', 'tipo_plano', 'imagen_portada'
    ]

    def test_func(self):
        # Solo administradores pueden editar
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        # Cuando termine de editar, lo regresamos a ver cómo quedó la sala
        return reverse_lazy('detalle_sala', kwargs={'pk': self.object.pk})

class ReservaListaView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas/reserva_lista.html'
    context_object_name = 'reservas'
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(usuario=self.request.user)
            .select_related('sala')
            .order_by('-fecha_inicio')
        )


class ReservaCrearView(LoginRequiredMixin, TemplateView):
    template_name = 'reservas/reserva_form_placeholder.html'


class CalendarioView(LoginRequiredMixin, TemplateView):
    template_name = 'reservas/calendario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas'] = (
            Reserva.objects.filter(usuario=self.request.user)
            .select_related('sala')
            .order_by('fecha_inicio')[:20]
        )
        return context