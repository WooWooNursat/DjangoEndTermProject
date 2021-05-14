from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from main.models import Order, Cart
from auth_.models import Client


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        client = instance.client
        products = Cart.objects.get(client=client).products
        instance.products.add(*products.values_list(flat=True))
        products.clear()


@receiver(post_save, sender=Client)
def client_created(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(client=instance)
