from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.tasks.models import Task


@login_required
def home(request):
    user = request.user

    if user.role == 'TEACHER' or user.role == 'STAFF' or user.role == 'PROGRAMMER':
        my_tasks = Task.objects.filter(assigned_by=user, is_personal=False)
        recent = my_tasks[:5]
        all_completed = my_tasks.filter(is_completed=True)
        recent_pending = my_tasks.filter(is_completed=False)[:3]
        personal_count = Task.objects.filter(assigned_by=user, is_personal=True, is_completed=False).count()
    else:
        my_tasks = Task.objects.filter(assigned_to=user, is_personal=False)
        recent = my_tasks[:5]
        all_completed = my_tasks.filter(is_completed=True)
        recent_pending = my_tasks.filter(is_completed=False)[:3]
        personal_count = 0

    pending = my_tasks.filter(is_completed=False).count()
    now = timezone.now()
    overdue = my_tasks.filter(is_completed=False, deadline__lt=now).count()

    completed_count = all_completed.count()
    level = completed_count // 5 + 1
    xp = completed_count % 5

    context = {
        'recent': recent,
        'pending': pending,
        'overdue': overdue,
        'recent_pending': recent_pending,
        'level': level,
        'xp': xp,
        'next_level_xp': 5,
        'completed_count': completed_count,
        'personal_count': personal_count,
    }

    return render(request, 'home.html', context)
