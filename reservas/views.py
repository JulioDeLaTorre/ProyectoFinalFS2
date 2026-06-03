from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.db import transaction

from .models import Reserva, Sala
from .forms import ReservaForm 

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
    
class ReservaCrearView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/reserva_form.html'
    success_url = reverse_lazy('lista_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenemos la sala de la URL o del parámetro GET
        sala_id = self.request.GET.get('sala')
        context['sala'] = Sala.objects.get(pk=sala_id)
        return context

    def form_valid(self, form):
        # 1. Obtenemos la instancia del formulario sin guardar aún
        reserva = form.save(commit=False)
        
        # 2. Asignamos la sala (que viene de la URL)
        sala_id = self.request.GET.get('sala')
        sala = Sala.objects.get(pk=sala_id)
        reserva.sala = sala
        
        # 3. Asignamos usuario y estado
        reserva.usuario = self.request.user
        reserva.estado_reserva = 'Confirmada'
        reserva.pagado = True
        
        # 4. CALCULO DEL COSTO (Aquí está la magia)
        # Si es por hora, tomamos precio_por_hora. Si es por día, precio_por_dia.
        if reserva.tipo_renta == 'Hora':
            reserva.costo_total = sala.precio_por_hora
        else:
            reserva.costo_total = sala.precio_por_dia
            
        # 5. Ahora guardamos la reserva con el costo ya calculado
        with transaction.atomic():
            reserva.save()
            
            # Cambiamos estado de la sala
            sala.estado = 'Inactiva'
            sala.save()
            
        messages.success(self.request, "¡Reserva confirmada con éxito!")
        return super().form_valid(form)