from django import forms
from reservas.models import Reserva
from huespedes.models import Huesped

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['huesped', 'fecha_entrada', 'fecha_salida', 'adultos', 'ninos', 'comentarios']
        widgets = {
            'huesped': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adultos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'ninos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }