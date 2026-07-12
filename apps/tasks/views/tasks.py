from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from apps.tasks.models import Task
from apps.tasks.forms import TaskForm, CommentForm
from apps.tasks.services import (
    get_task_queryset, apply_filters, create_task,
    complete_task, delete_task, add_comment,
)
from apps.accounts.decorators import role_required


@login_required
def task_list(request):
    user = request.user
    now = timezone.now()
    is_personal = request.GET.get('personal') == '1'

    tasks = get_task_queryset(user, is_personal=is_personal)
    tasks = apply_filters(tasks, request.GET, request.GET.get('status'), now)

    paginator = Paginator(tasks, 10)
    tasks_page = paginator.get_page(request.GET.get('page'))

    context = {
        'tasks': tasks_page,
        'can_assign': user.role in ('TEACHER', 'STAFF', 'PROGRAMMER'),
        'now': now,
        'urgent_date': now + timedelta(days=3),
        'importance_choices': Task.Importance.choices,
        'is_personal': is_personal,
        'user_role': user.role,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_personal(request):
    return task_list(request)


@login_required
def task_detail(request, pk):
    user = request.user

    if user.role in ('TEACHER', 'STAFF', 'PROGRAMMER'):
        task = get_object_or_404(
            Task.objects.select_related('assigned_to', 'assigned_by'),
            pk=pk, assigned_by=user,
        )
    else:
        task = get_object_or_404(
            Task.objects.select_related('assigned_to', 'assigned_by'),
            pk=pk, assigned_to=user,
        )

    comments = task.comments.select_related('user').all()
    comments_page = Paginator(comments, 10).get_page(request.GET.get('comment_page'))

    context = {
        'task': task,
        'can_assign': user.role in ('TEACHER', 'STAFF', 'PROGRAMMER'),
        'now': timezone.now(),
        'urgent_date': timezone.now() + timedelta(days=3),
        'user_role': user.role,
        'comments': comments_page,
        'form': CommentForm(),
    }
    return render(request, 'tasks/task_detail.html', context)


@role_required('TEACHER', 'STAFF', 'PROGRAMMER')
def task_create(request):
    personal = request.GET.get('personal') == '1'
    user = request.user

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            task = create_task(form, user, is_personal=personal)
            return redirect('task_personal' if personal else 'task_detail', pk=task.pk)
    else:
        form = TaskForm(user=user)

    return render(request, 'tasks/task_form.html', {'form': form, 'is_personal': personal})


@login_required
def task_complete(request, pk):
    if request.method != 'POST':
        return redirect('task_list')

    task = get_object_or_404(Task, pk=pk)

    if task.assigned_to != request.user and task.assigned_by != request.user:
        messages.error(request, 'No tenés permiso para completar esta tarea.')
        return redirect('task_list')

    complete_task(task, request.user)
    return redirect('task_personal' if task.is_personal else 'task_list')


@login_required
def task_delete(request, pk):
    if request.method != 'POST':
        return redirect('task_list')

    task = get_object_or_404(Task, pk=pk, assigned_by=request.user)
    personal, _ = delete_task(task)
    return redirect('task_personal' if personal else 'task_list')


@login_required
def comment_create(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.assigned_to != request.user and task.assigned_by != request.user:
        messages.error(request, 'No tenés permiso para comentar en esta tarea.')
        return redirect('task_list')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            add_comment(task, request.user, form.cleaned_data['text'])

    return redirect('task_detail', pk=pk)
