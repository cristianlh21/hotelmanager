from django.contrib import admin
from .models import Huesped

@admin.register(Huesped)
class HuespedAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'apellido',
        'tipo_documento',
        'numero_documento',
        'email',
        'telefono',
        'fecha_registro'
    ]
    list_filter = ['tipo_documento', 'pais', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'numero_documento', 'email']
    ordering = ['-fecha_registro']
    readonly_fields = ['fecha_registro']