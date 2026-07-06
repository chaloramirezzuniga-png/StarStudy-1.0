from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from apps.tasks.models import Task, Comment
from apps.accounts.models import Notification
from apps.tasks.forms import TaskForm, CommentForm


@login_required
def task_list(request):
    user = request.user
    now = timezone.now()

    if user.role == 'TEACHER' or user.role == 'STAFF' or user.role == 'PROGRAMMER':
        tasks = Task.objects.filter(assigned_by=user, is_personal=False)
    else:
        tasks = Task.objects.filter(assigned_to=user, is_personal=False)

    importance = request.GET.get('importance')
    if importance:
        tasks = tasks.filter(importance=importance)

    status = request.GET.get('status')
    if status == 'pending':
        tasks = tasks.filter(is_completed=False)
    elif status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status == 'overdue':
        tasks = tasks.filter(is_completed=False, deadline__lt=now)

    paginator = Paginator(tasks, 10)
    page = request.GET.get('page')
    tasks_page = paginator.get_page(page)

    can_assign = user.role == 'TEACHER' or user.role == 'STAFF' or user.role == 'PROGRAMMER'

    context = {
        'tasks': tasks_page,
        'can_assign': can_assign,
        'now': now,
        'urgent_date': now + timedelta(days=3),
        'importance_choices': Task.Importance.choices,
        'is_personal': False,
        'user_role': user.role,
    }

    return render(request, 'tasks/task_list.html', context)


@login_required
def task_personal(request):
    user = request.user
    now = timezone.now()

    tasks = Task.objects.filter(assigned_by=user, is_personal=True)

    importance = request.GET.get('importance')
    if importance:
        tasks = tasks.filter(importance=importance)

    status = request.GET.get('status')
    if status == 'pending':
        tasks = tasks.filter(is_completed=False)
    elif status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status == 'overdue':
        tasks = tasks.filter(is_completed=False, deadline__lt=now)

    paginator = Paginator(tasks, 10)
    page = request.GET.get('page')
    tasks_page = paginator.get_page(page)

    context = {
        'tasks': tasks_page,
        'can_assign': True,
        'now': now,
        'urgent_date': now + timedelta(days=3),
        'importance_choices': Task.Importance.choices,
        'is_personal': True,
        'user_role': user.role,
    }

    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    user = request.user

    if user.role == 'TEACHER' or user.role == 'STAFF' or user.role == 'PROGRAMMER':
        task = get_object_or_404(Task, pk=pk, assigned_by=user)
    else:
        task = get_object_or_404(Task, pk=pk, assigned_to=user)

    can_assign = user.role == 'TEACHER' or user.role == 'STAFF' or user.role == 'PROGRAMMER'
    comments = task.comments.all()
    form = CommentForm()

    context = {
        'task': task,
        'can_assign': can_assign,
        'now': timezone.now(),
        'urgent_date': timezone.now() + timedelta(days=3),
        'user_role': user.role,
        'comments': comments,
        'form': form,
    }

    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_create(request):
    personal = request.GET.get('personal') == '1'

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user

            if personal:
                task.is_personal = True
                task.assigned_to = request.user

            task.save()

            if not personal and task.assigned_to != request.user:
                Notification.objects.create(
                    user=task.assigned_to,
                    message=f'{request.user.get_full_name() or request.user.email} te asignó: {task.title}',
                    link=f'/tasks/{task.pk}/',
                )

            if personal:
                return redirect('task_personal')
            else:
                return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(user=request.user)

    context = {
        'form': form,
        'is_personal': personal,
    }

    return render(request, 'tasks/task_form.html', context)


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.assigned_to != request.user and task.assigned_by != request.user:
        return redirect('task_list')

    task.is_completed = True
    task.completed_at = timezone.now()
    task.save()

    if not task.is_personal:
        Notification.objects.create(
            user=task.assigned_by,
            message=f'{request.user.get_full_name() or request.user.email} completó: {task.title}',
            link=f'/tasks/{task.pk}/',
        )

    if task.is_personal:
        return redirect('task_personal')
    else:
        return redirect('task_list')


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_by=request.user)
    personal = task.is_personal
    task.delete()

    if personal:
        return redirect('task_personal')
    else:
        return redirect('task_list')


@login_required
def comment_create(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.assigned_to != request.user and task.assigned_by != request.user:
        return redirect('task_list')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()

    return redirect('task_detail', pk=pk)
