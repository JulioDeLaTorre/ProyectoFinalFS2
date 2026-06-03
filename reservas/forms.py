from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['tipo_renta', 'fecha_inicio', 'fecha_fin'] # Sala la pasaremos por código
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_fecha_inicio'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'id_fecha_fin', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyectamos el JS directamente al formulario
        self.fields['tipo_renta'].widget.attrs.update({'onchange': 'calcularFechaFin()'})
        self.fields['fecha_inicio'].widget.attrs.update({'onchange': 'calcularFechaFin()'})


class ReservaMoverForm(forms.ModelForm):
    """Formulario para cambiar solo la fecha de inicio de una reserva existente."""
    class Meta:
        model = Reserva
        fields = ['fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['fecha_inicio'].label = 'Nueva fecha de inicio'