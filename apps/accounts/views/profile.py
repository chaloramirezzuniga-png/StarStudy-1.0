"""Vistas de perfil: información del usuario, vinculación, GitHub y notificaciones.

- profile: muestra stats del perfil; estudiantes pueden vincularse con código.
- github_connect / github_disconnect: gestiona cuenta GitHub (solo programadores).
- notification_list: lista paginada de notificaciones.
- notification_read: marca notificación como leída (POST-only, CSRF).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from apps.accounts.models import User, Notification
from apps.accounts.services import (
    get_user_stats, link_student_to_teacher,
    connect_github, disconnect_github, mark_notification_read,
)


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST' and user.role == User.Role.STUDENT:
        code = request.POST.get('code', '')
        success, teacher = link_student_to_teacher(user, code)
        if success:
            messages.success(request, 'Vinculado a ' + (teacher.get_full_name() or teacher.email))
        else:
            messages.error(request, 'Código inválido')
        return redirect('profile')

    context = get_user_stats(user)
    return render(request, 'accounts/profile.html', context)


@login_required
def github_connect(request):
    if request.user.role != User.Role.PROGRAMMER:
        messages.error(request, 'Solo programadores pueden conectar GitHub.')
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('github_username', '')
        if connect_github(request.user, username):
            messages.success(request, f'Cuenta de GitHub @{username.strip()} conectada.')
        else:
            messages.error(request, 'Ingresá un nombre de usuario de GitHub.')
    return redirect('profile')


@login_required
def github_disconnect(request):
    disconnect_github(request.user)
    messages.success(request, 'Cuenta de GitHub desconectada.')
    return redirect('profile')


NOTIF_FIELDS = ['id', 'message', 'link', 'is_read', 'created_at']

@login_required
def notification_list(request):
    notifs = request.user.notifications.all().only(*NOTIF_FIELDS)
    notifs_page = Paginator(notifs, 20).get_page(request.GET.get('page'))
    return render(request, 'accounts/notification_list.html', {'notifications': notifs_page})


@login_required
def notification_read(request, pk):
    if request.method != 'POST':
        return redirect('notification_list')
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    mark_notification_read(notif)
    return redirect(notif.link) if notif.link else redirect('notification_list')
