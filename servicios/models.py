# apps/servicios/models.py
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

class Servicio(models.Model):
    """Catálogo de servicios extra que ofrece el hotel"""
    
    TIPOS_SERVICIO = [
        ('alimentos', 'Alimentos & Bebidas'),
        ('estacionamiento', 'Estacionamiento'),
        ('lavanderia', 'Lavandería'),
        ('late_checkout', 'Late Check-out'),
        ('early_checkin', 'Early Check-in'),
        ('otros', 'Otros'),
    ]
    
    nombre = models.CharField(max_length=50)          # "Desayuno completo"
    tipo = models.CharField(max_length=20, choices=TIPOS_SERVICIO)
    precio_unitario = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Unidades de venta
    UNIDADES = [
        ('unidad', 'Unidad'),
        ('dia', 'Por día'),
        ('hora', 'Por hora'),
        ('persona', 'Por persona'),
        ('noche', 'Por noche'),
    ]
    unidad = models.CharField(max_length=10, choices=UNIDADES, default='unidad')
    
    descripcion = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'servicios_servicio'
        ordering = ['tipo', 'nombre']

    def __str__(self):
        return f"{self.nombre} (${self.precio_unitario} / {self.get_unidad_display()})"

class Consumo(models.Model):
    """Servicios consumidos por una reserva/huésped"""
    
    reserva = models.ForeignKey(
        'reservas.Reserva',
        on_delete=models.CASCADE,
        related_name='consumos'
    )
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
    cantidad = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    fecha_consumo = models.DateTimeField(auto_now_add=True)
    notas = models.CharField(max_length=200, blank=True)
    
    # Si lo facturás aparte
    facturado = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'servicios_consumo'
        ordering = ['-fecha_consumo']

    def __str__(self):
        return f"{self.servicio.nombre} x{self.cantidad} - {self.reserva}"

    def save(self, *args, **kwargs):
        # Calcula el total automáticamente
        self.precio_total = self.servicio.precio_unitario * self.cantidad
        super().save(*args, **kwargs)