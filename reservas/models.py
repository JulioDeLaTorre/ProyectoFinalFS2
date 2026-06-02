import uuid
from django.conf import settings
from django.db import models


class Sala(models.Model):
    ESTADOS_SALA = (
        ('Disponible', 'Disponible'),
        ('Mantenimiento', 'En Mantenimiento'),
        ('Inactiva', 'Inactiva'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    ubicacion = models.CharField(
        max_length=150,
        default='Sin ubicación',
        verbose_name='Ubicación'
    )

    capacidad_maxima = models.IntegerField()
    precio_por_hora = models.DecimalField(max_digits=8, decimal_places=2)
    precio_por_dia = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_SALA,
        default='Disponible'
    )

    imagen_portada = models.ImageField(
        upload_to='salas_portadas/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    TIPOS_RENTA = (
        ('Hora', 'Por Hora'),
        ('Dia', 'Por Día'),
    )

    ESTADOS_RESERVA = (
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    sala = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tipo_renta = models.CharField(max_length=10, choices=TIPOS_RENTA)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_reserva = models.CharField(
        max_length=20,
        choices=ESTADOS_RESERVA,
        default='Pendiente'
    )
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva: {self.sala.nombre} - {self.usuario.username}"