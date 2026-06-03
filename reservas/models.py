import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class Sala(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ubicacion = models.CharField(
        max_length=150,
        default='Sin ubicación',
        verbose_name='Ubicación',
    )
    capacidad_maxima = models.IntegerField()
    precio_por_hora = models.DecimalField(max_digits=8, decimal_places=2)
    precio_por_dia = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Disponible', 'Disponible'),
            ('Mantenimiento', 'En Mantenimiento'),
            ('Inactiva', 'Inactiva'),
        ],
        default='Disponible',
    )
    
    tipo_plano = models.CharField(
        max_length=20,
        choices=[
            ('oficina', 'Oficina / Sala de Juntas'),
            ('fiesta', 'Salón de Fiestas'),
            ('cine', 'Auditorio / Cine'),
        ],
        default='oficina',
        verbose_name='Tipo de Plano (Visual)'
    )
    
    imagen_portada = models.ImageField(
        upload_to='salas_portadas/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_sala', kwargs={'pk': self.pk})

class Reserva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sala = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tipo_renta = models.CharField(
        max_length=10,
        choices=[
            ('Hora', 'Por Hora'),
            ('Dia', 'Por Día'),
        ],
    )
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_reserva = models.CharField(
        max_length=20,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Confirmada', 'Confirmada'),
            ('Cancelada', 'Cancelada'),
        ],
        default='Pendiente',
    )
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reserva de {self.usuario} en {self.sala}'

    def get_absolute_url(self):
        return reverse('lista_reservas')


class SalaCrearView(UserPassesTestMixin, CreateView):
    model = Sala
    template_name = 'reservas/sala_form.html'
    # Campos que mostraremos en el formulario
    fields = [
        'nombre', 'descripcion', 'ubicacion', 'capacidad_maxima', 
        'precio_por_hora', 'precio_por_dia', 'estado', 'tipo_plano', 'imagen_portada'
    ]
    success_url = reverse_lazy('lista_salas')

    # Esta función es el "cadenero". Si regresa False, bloquea el acceso (Error 403)
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
