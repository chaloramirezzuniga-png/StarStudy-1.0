from datetime import date, datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.utils.timezone import now

scheduler = BackgroundScheduler()
_started = False


def check_habit_notifications():
    from core.base.models import Habit, Notification

    today = date.today()
    now_time = datetime.now().time()
    window_start = (datetime.combine(today, now_time) - timedelta(minutes=1)).time()
    window_end = (datetime.combine(today, now_time) + timedelta(minutes=1)).time()

    habits = Habit.objects.select_related('user').all()

    for habit in habits:
        for time_field, tipo in [(habit.start_time, 'inicio'), (habit.end_time, 'fin')]:
            if window_start <= time_field <= window_end:
                notif_key = f"habito_{tipo}_{habit.pk}_{today}"
                already_sent = Notification.objects.filter(
                    user=habit.user,
                    message__startswith=f"[{notif_key}]"
                ).exists()
                if not already_sent:
                    msg_map = {'inicio': f'[{notif_key}] ¡Hora de comenzar "{habit.title}"!',
                               'fin': f'[{notif_key}] ¡Hora de terminar "{habit.title}"!'}
                    Notification.objects.create(
                        user=habit.user,
                        message=msg_map[tipo],
                        link='/habitos/'
                    )


def check_task_deadlines():
    from core.base.models import Task, Notification
    from django.utils import timezone

    now_dt = timezone.now()
    one_min_ago = now_dt - timedelta(minutes=1)

    expiring = Task.objects.filter(
        is_completed=False,
        deadline__gte=one_min_ago,
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
            Notification.objects.create(
                user=task.assigned_by,
                message=f'[{notif_key}] Vence hoy: "{task.title}" de {task.assigned_to.get_full_name() or task.assigned_to.email}',
                link=f'/tasks/{task.pk}/',
            )


def start():
    global _started
    if _started:
        return
    try:
        scheduler.add_job(check_habit_notifications, 'interval', minutes=1, id='habits', replace_existing=True)
        scheduler.add_job(check_task_deadlines, 'interval', minutes=1, id='deadlines', replace_existing=True)
        scheduler.start()
        _started = True
    except Exception:
        pass
