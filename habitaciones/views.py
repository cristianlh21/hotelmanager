from django.shortcuts import render
from .models import Habitacion

def dashboard_recepcion(request):
    """Muestra TODAS las habitaciones"""
    habitaciones = Habitacion.objects.all().order_by('numero')
    return render(request, 'habitaciones/dashboard.html', {'habitaciones': habitaciones})