from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from auth_.models import Card, Client, MainUser, Profile


@receiver(post_save, sender=MainUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Client)
def user_created(sender, instance, created, **kwargs):
    if created:
        instance.card = Card.objects.create()
