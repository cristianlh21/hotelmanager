from django.contrib import admin
from .models import TipoHabitacion, Habitacion, CanalVenta, Tarifa

@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio_por_noche', 'max_personas']  # Quité 'activo'
    search_fields = ['nombre']
    list_editable = ['precio_por_noche']

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'tipo', 'estado']  # Quité 'precio_actual'
    list_filter = ['estado', 'tipo']
    search_fields = ['numero']
    list_editable = ['estado']

@admin.register(CanalVenta)
class CanalVentaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'es_online', 'comision_porcentaje']

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ['tipo_habitacion', 'canal', 'precio_noche', 'fecha_inicio', 'fecha_fin', 'activa']
    list_filter = ['canal', 'activa']
    search_fields = ['tipo_habitacion__nombre']