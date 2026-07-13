"""Scheduler APScheduler: tareas en background para notificaciones.

- check_habit_notifications: cada 1 min, verifica hábitos con hora de inicio/fin
  dentro de ventana de ±2 min. Crea notificación si no fue enviada hoy.
- check_task_deadlines: cada 1 min, verifica tareas no personales que vencen hoy
  (deadline en últimos 2 min). Notifica al creador de la tarea.
- start: inicia el scheduler (solo una vez). Se llama desde AppConfig.ready().
"""
import logging
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
_started = False


def check_habit_notifications():
    from apps.habits.models import Habit
    from apps.accounts.models import Notification
    from apps.accounts.cache import invalidate_unread

    now_dt = timezone.now()
    today = now_dt.date()
    now_time = now_dt.time()
    window_start = (now_dt - timedelta(minutes=2)).time()
    window_end = (now_dt + timedelta(minutes=2)).time()

    habits = Habit.objects.select_related('user').all()

    for habit in habits:
        if habit.start_time == habit.end_time and habit.start_time.hour == 0 and habit.start_time.minute == 0:
            continue
        for time_field, tipo in [(habit.start_time, 'inicio'), (habit.end_time, 'fin')]:
            in_window = (window_start <= time_field <= window_end) if window_start <= window_end else (time_field >= window_start or time_field <= window_end)
            if in_window:
                notif_key = f"habito_{tipo}_{habit.pk}_{today}"
                already_sent = Notification.objects.filter(
                    user=habit.user,
                    message__startswith=f"[{notif_key}]"
                ).exists()
                if not already_sent:
                    msg_map = {'inicio': f'[{notif_key}] ¡Hora de comenzar "{habit.title}"!',
                               'fin': f'[{notif_key}] ¡Hora de terminar "{habit.title}"!'}
                    with transaction.atomic():
                        Notification.objects.create(
                            user=habit.user,
                            message=msg_map[tipo],
                            link='/habitos/'
                        )
                    invalidate_unread(habit.user)


def check_task_deadlines():
    from apps.tasks.models import Task
    from apps.accounts.models import Notification
    from apps.accounts.cache import invalidate_unread

    now_dt = timezone.now()
    two_min_ago = now_dt - timedelta(minutes=2)

    expiring = Task.objects.filter(
        is_completed=False,
        deadline__gte=two_min_ago,
        deadline__lte=now_dt,
        is_personal=False,
    ).select_related('assigned_by', 'assigned_to')

    for task in expiring:
        notif_key = f"deadline_{task.pk}_{task.deadline.date()}"
        already_sent = Notification.objects.filter(
            user=task.assigned_by,
            message__startswith=f"[{notif_key}]"
        ).exists()
        if not already_sent:
            with transaction.atomic():
                Notification.objects.create(
                    user=task.assigned_by,
                    message=f'[{notif_key}] Vence hoy: "{task.title}" de {task.assigned_to.get_full_name() or task.assigned_to.email}',
                    link=f'/tasks/{task.pk}/',
                )
            invalidate_unread(task.assigned_by)


def start():
    global _started
    if _started:
        return
    try:
        scheduler.add_job(check_habit_notifications, 'interval', minutes=1, id='habits', replace_existing=True)
        scheduler.add_job(check_task_deadlines, 'interval', minutes=1, id='deadlines', replace_existing=True)
        scheduler.start()
        _started = True
    except Exception as e:
        logger.exception('Error al iniciar el scheduler: %s', e)
