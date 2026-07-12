from django.db.models import Count, Q
from apps.accounts.models import User, Notification
from apps.accounts.cache import (
    get_profile_stats, invalidate_profile,
    invalidate_unread, invalidate_home,
)


def get_user_stats(user):
    from apps.tasks.models import Task

    can_assign = user.role in ('TEACHER', 'STAFF', 'PROGRAMMER')

    def fetch():
        task_stats = Task.objects.filter(
            Q(assigned_by=user) | Q(assigned_to=user)
        ).aggregate(
            assigned=Count('id', filter=Q(assigned_by=user, is_personal=False)),
            completed=Count('id', filter=Q(assigned_to=user, is_completed=True)),
            pending=Count('id', filter=Q(assigned_to=user, is_completed=False)),
        )
        students = list(user.linked_students.all()) if can_assign else []
        return {
            'assigned': task_stats['assigned'],
            'completed': task_stats['completed'],
            'pending': task_stats['pending'],
            'students': students,
        }

    return get_profile_stats(user.pk, fetch)


def link_student_to_teacher(user, code):
    code = code.strip().upper()
    teacher = User.objects.filter(code=code).exclude(role=User.Role.STUDENT).first()
    if teacher:
        user.linked_to = teacher
        user.save(update_fields=['linked_to'])
        return True, teacher
    return False, None


def connect_github(user, username):
    username = username.strip()
    if not username:
        return False
    user.github_username = username
    user.save(update_fields=['github_username'])
    return True


def disconnect_github(user):
    user.github_username = None
    user.github_token = None
    user.save(update_fields=['github_username', 'github_token'])


def mark_notification_read(notification):
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    invalidate_unread(notification.user)
    return notification
