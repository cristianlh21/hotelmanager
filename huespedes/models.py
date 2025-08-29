from django.db import models
from django.contrib.auth.models import User

class Huesped(models.Model):
    """Modelo principal de huéspedes"""
    TIPO_DOCUMENTO = [
        ('dni', 'DNI'),
        ('pasaporte', 'Pasaporte'),
        ('cuit', 'CUIT'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField()
    ciudad = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'huespedes_huesped'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"