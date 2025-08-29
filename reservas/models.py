from django.db import models
from django.utils import timezone

class Reserva(models.Model):
    """Reservaciones principales"""
    ESTADOS = [
        ('pendiente', 'Pendiente Confirmación'),
        ('confirmada', 'Confirmada'),
        ('check_in', 'Check-in Realizado'),
        ('check_out', 'Check-out Realizado'),
        ('cancelada', 'Cancelada'),
        ('no_show', 'No Show'),
    ]
    
    # Relaciones con otras apps
    huesped = models.ForeignKey('huespedes.Huesped', on_delete=models.CASCADE)
    habitacion = models.ForeignKey('habitaciones.Habitacion', on_delete=models.CASCADE)
    
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    
    # Información de reserva
    adultos = models.PositiveIntegerField(default=1)
    ninos = models.PositiveIntegerField(default=0)
    comentarios = models.TextField(blank=True)
    
    class Meta:
        db_table = 'reservas_reserva'
        indexes = [
            models.Index(fields=['fecha_entrada', 'fecha_salida']),
            models.Index(fields=['estado']),
        ]
    
    @property
    def noches(self):
        return (self.fecha_salida - self.fecha_entrada).days

class HuespedAdicional(models.Model):
    """Acompañantes en la reserva"""
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='acompanantes')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=10)
    numero_documento = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    
    class Meta:
        db_table = 'reservas_huespedadicional'