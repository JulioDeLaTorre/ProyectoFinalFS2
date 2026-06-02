from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, TemplateView

from .models import Reserva, Sala


class InicioView(TemplateView):
    template_name = 'inicio.html'


class SalaListaView(ListView):
    model = Sala
    template_name = 'reservas/sala_lista.html'
    context_object_name = 'salas'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(ubicacion__icontains=q))
        return qs


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
