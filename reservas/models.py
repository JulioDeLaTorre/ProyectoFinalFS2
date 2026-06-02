from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Sala(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    capacidad = models.IntegerField()
    precio_por_hora = models.DecimalField(max_digits=8, decimal_places=2)
    # Requiere instalar Pillow (pip install Pillow)
    imagen = models.ImageField(upload_to='salas/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_sala', kwargs={'pk': self.pk})

class Reserva(models.Model):
    # Aquí están las pistas exactas de tu profesor
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Lo mínimo necesario para saber cuándo rentan
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    
    # Fecha en la que se hizo el clic de reservar
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reserva de {self.usuario} en {self.sala}'
    
    def get_absolute_url(self):
        return reverse('lista_reservas')
