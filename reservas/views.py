from django.shortcuts import render, redirect, get_object_or_404
from habitaciones.models import Habitacion
from huespedes.models import Huesped
from reservas.models import Reserva
from django import forms

# Paso 1: elegir huésped o crear nuevo
def seleccionar_huesped(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    
    if request.method == 'POST':
        # Puede venir "huesped_existente" o "crear_nuevo"
        if 'huesped_existente' in request.POST:
            huesped_id = request.POST['huesped_existente']
            return redirect('crear_reserva', habitacion_id=habitacion_id, huesped_id=huesped_id)
        elif 'crear_nuevo' in request.POST:
            return redirect('crear_huesped_y_reserva', habitacion_id=habitacion_id)
    
    huespedes = Huesped.objects.all()
    return render(request, 'reservas/seleccionar_huesped.html', {
        'habitacion': habitacion,
        'huespedes': huespedes,
    })

# Paso 2: crear huésped rápido y reserva
def crear_huesped_y_reserva(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    
    class HuespedReservaForm(forms.Form):
        tipo_documento = forms.ChoiceField(choices=Huesped.TIPO_DOCUMENTO, widget=forms.Select(attrs={'class': 'form-select'}))
        numero_documento = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
        nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
        apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
        email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
        telefono = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
        fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
        fecha_entrada = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
        fecha_salida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
        adultos = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
        ninos = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
        comentarios = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))

    if request.method == 'POST':
        form = HuespedReservaForm(request.POST)
        if form.is_valid():
            # Crear huésped
            huesped, _ = Huesped.objects.get_or_create(
                numero_documento=form.cleaned_data['numero_documento'],
                defaults={
                    'tipo_documento': form.cleaned_data['tipo_documento'],
                    'nombre': form.cleaned_data['nombre'],
                    'apellido': form.cleaned_data['apellido'],
                    'email': form.cleaned_data['email'],
                    'telefono': form.cleaned_data['telefono'],
                    'fecha_nacimiento': form.cleaned_data['fecha_nacimiento'],
                }
            )
            # Crear reserva
            Reserva.objects.create(
                huesped=huesped,
                habitacion=habitacion,
                fecha_entrada=form.cleaned_data['fecha_entrada'],
                fecha_salida=form.cleaned_data['fecha_salida'],
                adultos=form.cleaned_data['adultos'],
                ninos=form.cleaned_data['ninos'],
                comentarios=form.cleaned_data['comentarios']
            )
            return redirect('dashboard_recepcion')
    else:
        form = HuespedReservaForm()
    
    return render(request, 'reservas/crear_huesped_reserva.html', {
        'form': form,
        'habitacion': habitacion
    })