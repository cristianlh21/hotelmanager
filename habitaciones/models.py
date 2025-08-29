# apps/habitaciones/models.py  (versión final con tarifas)
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    precio_por_noche = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.00'))]
    )
    max_personas = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'habitaciones_tipo'

    def __str__(self):
        return f"{self.nombre} - ${self.precio_por_noche}"

class Habitacion(models.Model):
    numero = models.CharField(max_length=5, unique=True)
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)

    ESTADOS = [
        ('disponible', 'Disponible'),
        ('reservada', 'Reservada'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
        ('sucia', 'Necesita Limpieza'),
    ]
    estado = models.CharField(max_length=15, choices=ESTADOS, default='disponible')
    notas = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'habitaciones_habitacion'
        ordering = ['numero']

    def __str__(self):
        return f"H{self.numero} ({self.tipo.nombre})"

    def get_precio_para_canal(self, canal, fecha=None):
        """Precio vigente de esta habitación para un canal y fecha."""
        if fecha is None:
            from datetime import date
            fecha = date.today()

        tarifa = Tarifa.objects.filter(
            tipo_habitacion=self.tipo,
            canal=canal,
            fecha_inicio__lte=fecha,
            fecha_fin__gte=fecha,
            activa=True
        ).first()

        return tarifa.precio_noche if tarifa else self.tipo.precio_por_noche

class CanalVenta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    es_online = models.BooleanField(default=False)
    comision_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="% de comisión que te cobra el canal"
    )

    class Meta:
        db_table = 'habitaciones_canalventa'
        verbose_name_plural = "Canales de Venta"

    def __str__(self):
        return self.nombre

class Tarifa(models.Model):
    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        on_delete=models.CASCADE,
        related_name='tarifas'
    )
    canal = models.ForeignKey(
        CanalVenta,
        on_delete=models.CASCADE,
        related_name='tarifas'
    )
    precio_noche = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.00'))]
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'habitaciones_tarifa'
        unique_together = ('tipo_habitacion', 'canal', 'fecha_inicio', 'fecha_fin')
        ordering = ['tipo_habitacion', 'canal', '-fecha_inicio']

    def __str__(self):
        return f"{self.tipo_habitacion.nombre} - {self.canal.nombre}: ${self.precio_noche}"

    def esta_vigente(self, fecha=None):
        from datetime import date
        if fecha is None:
            fecha = date.today()
        return self.fecha_inicio <= fecha <= self.fecha_fin and self.activa