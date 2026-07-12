from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from apps.accounts.models import User
from apps.accounts.cache import get_home_stats, invalidate_home
from apps.tasks.models import Task


@login_required
def home(request):
    user = request.user
    now = timezone.now()
    is_student = user.role == User.Role.STUDENT

    def fetch_stats():
        HOME_FIELDS = ['id', 'title', 'importance', 'deadline', 'is_completed', 'is_personal', 'assigned_to_id', 'assigned_by_id']
        base_tasks = Task.objects.select_related('assigned_to', 'assigned_by').only(*HOME_FIELDS)

        if is_student:
            base_tasks = base_tasks.filter(assigned_to=user, is_personal=False)
        else:
            base_tasks = base_tasks.filter(assigned_by=user, is_personal=False)

        counts = base_tasks.aggregate(
            pending=Count('id', filter=Q(is_completed=False)),
            overdue=Count('id', filter=Q(is_completed=False, deadline__lt=now)),
            completed=Count('id', filter=Q(is_completed=True)),
            personal=Count('id', filter=Q(is_personal=True, is_completed=False)),
        )

        recent = list(base_tasks.filter(is_completed=False).order_by('deadline')[:5])
        recent_pending = list(base_tasks.filter(is_completed=False).order_by('deadline')[:3])

        counts['recent'] = recent
        counts['recent_pending'] = recent_pending
        return counts

    stats = get_home_stats(user.pk, fetch_stats)

    completed_count = stats['completed']
    level = completed_count // 5 + 1
    xp = completed_count % 5

    context = {
        'recent': stats['recent'],
        'pending': stats['pending'],
        'overdue': stats['overdue'],
        'recent_pending': stats['recent_pending'],
        'level': level,
        'xp': xp,
        'next_level_xp': 5,
        'completed_count': completed_count,
        'personal_count': stats['personal'],
    }

    return render(request, 'home.html', context)
