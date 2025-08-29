from django.contrib import admin
from .models import Servicio, Consumo

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'precio_unitario', 'unidad', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre']

@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
    list_display = ['reserva', 'servicio', 'cantidad', 'precio_total', 'fecha_consumo']
    readonly_fields = ['precio_total', 'fecha_consumo']