from django.shortcuts import render, redirect, get_object_or_404
from reservas.forms import ReservaForm
from habitaciones.models import Habitacion
from reservas.models import Reserva

def reserva_nueva(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.habitacion = habitacion
            reserva.save()
            return redirect('dashboard_recepcion')  # volver al dashboard
    else:
        form = ReservaForm()

    return render(request, 'reservas/reserva_form.html', {
        'form': form,
        'habitacion': habitacion
    })