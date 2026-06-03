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