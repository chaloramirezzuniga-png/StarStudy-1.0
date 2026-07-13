from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User, Notification
from apps.accounts.cache import invalidate_unread


@receiver(post_save, sender=User)
def notificar_bienvenida(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            message='¡Bienvenido a StarStudy! Empezá explorando tu perfil.',
            link='/profile/',
        )
        invalidate_unread(instance)
