from django.contrib import admin
from .models import Reserva, HuespedAdicional

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'huesped', 'habitacion', 'fecha_entrada', 'fecha_salida', 'estado']
    list_filter = ['estado', 'fecha_entrada']
    search_fields = ['huesped__nombre', 'habitacion__numero']
    date_hierarchy = 'fecha_entrada'

@admin.register(HuespedAdicional)
class HuespedAdicionalAdmin(admin.ModelAdmin):
    list_display = ['reserva', 'nombre', 'apellido', 'tipo_documento', 'numero_documento']
    search_fields = ['nombre', 'apellido', 'numero_documento']