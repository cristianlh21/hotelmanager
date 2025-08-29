from django.db.models.signals import post_save
from django.dispatch import receiver
from reservas.models import Reserva
from facturacion.models import Factura

@receiver(post_save, sender=Reserva)
def generar_factura_al_checkin(sender, instance, **kwargs):
    """Cuando la reserva pasa a 'check_in', crea la factura"""
    if instance.estado == 'check_in':
        # Verificar que no exista ya una factura
        if not hasattr(instance, 'factura'):
            subtotal = instance.habitacion.tipo.precio_por_noche * instance.noches
            impuestos = subtotal * 0.21  # IVA 21%
            total = subtotal + impuestos
            
            Factura.objects.create(
                reserva=instance,
                numero=f"F{instance.id}-{timezone.now().strftime('%Y%m%d')}",
                subtotal=subtotal,
                impuestos=impuestos,
                total=total,
                estado='pendiente'
            )
            
@receiver(post_save, sender=Reserva)
def actualizar_estado_habitacion(sender, instance, **kwargs):
    """Cambia el estado de la habitación según la reserva"""
    if instance.estado == 'pendiente':
        instance.habitacion.estado = 'reservada'
    elif instance.estado == 'confirmada':
        instance.habitacion.estado = 'reservada'
    elif instance.estado == 'check_in':
        instance.habitacion.estado = 'ocupada'
    elif instance.estado == 'check_out':
        instance.habitacion.estado = 'disponible'
    elif instance.estado == 'cancelada':
        instance.habitacion.estado = 'disponible'
    instance.habitacion.save()