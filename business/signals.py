from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *


@receiver(post_save,sender=BusinessInflow)
def send_quantity_left(sender, instance, **kwargs):
    instance.sold_item.update_quantity_left()

@receiver(post_delete, sender=BusinessInflow)
def update_quantity_left_on_delete(sender, instance, **kwargs):
    instance.sold_item.update_quantity_left()