from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.utils import timezone
from datetime import timedelta
from .models import OrderLineItem, Order
from homepage.models import UserProfile
from admin_dashboard.models import OrderDeletionRecord


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()


@receiver(post_save, sender=OrderDeletionRecord)
def cleanup_old_orders(sender, **kwargs):
    """Delete pending orders older than 3 days."""
    one_day_ago = timezone.now() - timedelta(days=3)
    orders_to_delete = Order.objects.filter(
        status=0,
        date__lt=one_day_ago,
    )

    if orders_to_delete is not None:
        orders_to_delete.delete()
