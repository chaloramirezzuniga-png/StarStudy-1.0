from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.tasks.models import Task
from apps.accounts.models import Notification
from apps.accounts.cache import invalidate_unread


@receiver(post_save, sender=Task)
def notificar_tarea_asignada(sender, instance, created, **kwargs):
    if created and not instance.is_personal and instance.assigned_to != instance.assigned_by:
        Notification.objects.create(
            user=instance.assigned_to,
            message=f'{instance.assigned_by.get_full_name() or instance.assigned_by.email} te asignó: {instance.title}',
            link=f'/tasks/{instance.pk}/',
        )
        invalidate_unread(instance.assigned_to)
