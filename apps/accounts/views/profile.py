from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from apps.accounts.models import User, Notification
from apps.tasks.models import Task


@login_required
def profile(request):
    user = request.user
    can_assign = user.role == 'TEACHER' or user.role == 'STAFF' or user.role == 'PROGRAMMER'

    if can_assign:
        assigned = Task.objects.filter(assigned_by=user).count()
    else:
        assigned = 0

    completed = Task.objects.filter(assigned_to=user, is_completed=True).count()
    pending_tasks = Task.objects.filter(assigned_to=user, is_completed=False).count()

    if request.method == 'POST' and user.role == User.Role.STUDENT:
        code = request.POST.get('code', '').strip().upper()
        teacher = User.objects.filter(code=code).exclude(role=User.Role.STUDENT).first()

        if teacher:
            user.linked_to = teacher
            user.save()
            messages.success(request, 'Vinculado a ' + (teacher.get_full_name() or teacher.email))
        else:
            messages.error(request, 'Código inválido')

        return redirect('profile')

    if can_assign:
        students = user.linked_students.all()
    else:
        students = []

    context = {
        'assigned': assigned,
        'completed': completed,
        'pending': pending_tasks,
        'students': students,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def github_connect(request):
    if request.user.role != User.Role.PROGRAMMER:
        messages.error(request, 'Solo programadores pueden conectar GitHub.')
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('github_username', '').strip()
        if username:
            request.user.github_username = username
            request.user.save(update_fields=['github_username'])
            messages.success(request, f'Cuenta de GitHub @{username} conectada.')
        else:
            messages.error(request, 'Ingresá un nombre de usuario de GitHub.')
    return redirect('profile')


@login_required
def github_disconnect(request):
    request.user.github_username = None
    request.user.github_token = None
    request.user.save(update_fields=['github_username', 'github_token'])
    messages.success(request, 'Cuenta de GitHub desconectada.')
    return redirect('profile')


@login_required
def notification_list(request):
    notifs = request.user.notifications.all()
    paginator = Paginator(notifs, 20)
    page = request.GET.get('page')
    notifs_page = paginator.get_page(page)
    context = {'notifications': notifs_page}
    return render(request, 'accounts/notification_list.html', context)


@login_required
def notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('notification_list')
