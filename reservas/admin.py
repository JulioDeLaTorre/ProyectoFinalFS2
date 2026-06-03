from django.contrib import admin
from .models import Sala, Reserva

# Register your models here.
@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'ubicacion',
        'capacidad_maxima',
        'precio_por_hora',
        'precio_por_dia',
        'tipo_plano',
        'estado',
    )
    search_fields = (
        'nombre',
        'ubicacion',
    )
    list_filter = (
        'estado',
    )


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'sala',
        'usuario',
        'fecha_inicio',
        'fecha_fin',
        'tipo_renta',
        'estado_reserva',
        'pagado',
    )
    search_fields = (
        'sala__nombre',
        'usuario__username',
        'usuario__email',
    )
    list_filter = (
        'estado_reserva',
        'tipo_renta',
        'pagado',
    )