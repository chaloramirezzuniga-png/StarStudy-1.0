from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.base.models import User, ScheduleEntry
from core.roles.forms import ScheduleEntryForm
from core.roles.utils import build_schedule_table


@login_required
def schedule_personal(request):
    user = request.user
    day_values = [d.value for d in ScheduleEntry.Day]

    if request.method == 'POST' and 'delete_id' in request.POST:
        ScheduleEntry.objects.filter(pk=request.POST['delete_id'], user=user).delete()
        return redirect('schedule_personal')

    form = ScheduleEntryForm(request.POST or None, user=user)
    if request.method == 'POST' and 'add' in request.POST:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = user
            entry.schedule_type = ScheduleEntry.ScheduleType.PERSONAL
            entry.save()
            return redirect('schedule_personal')

    all_entries = list(ScheduleEntry.objects.filter(user=user, schedule_type=ScheduleEntry.ScheduleType.PERSONAL))
    rows = build_schedule_table(all_entries, day_values)

    context = {
        'form': form,
        'rows': rows,
        'days': list(ScheduleEntry.Day),
        'all_entries': all_entries,
        'schedule_name': 'Personal',
        'readonly': False,
        'user_role': user.role,
    }

    return render(request, 'core/schedule_personal.html', context)


@login_required
def schedule_student_course(request):
    user = request.user
    teacher = user.linked_to

    if not teacher:
        messages.error(request, 'No estás vinculado a ningún profesor.')
        return redirect('schedule_personal')

    day_values = [d.value for d in ScheduleEntry.Day]

    all_entries = list(ScheduleEntry.objects.filter(
        user=teacher,
        schedule_type=ScheduleEntry.ScheduleType.COURSE
    ))
    rows = build_schedule_table(all_entries, day_values)

    context = {
        'rows': rows,
        'days': list(ScheduleEntry.Day),
        'all_entries': all_entries,
        'schedule_name': 'del Curso',
        'readonly': True,
        'user_role': user.role,
    }

    return render(request, 'core/schedule_personal.html', context)


@login_required
def schedule_course(request):
    if request.user.role != User.Role.TEACHER:
        return redirect('schedule_student_course')

    user = request.user
    day_values = [d.value for d in ScheduleEntry.Day]

    if request.method == 'POST' and 'delete_id' in request.POST:
        ScheduleEntry.objects.filter(pk=request.POST['delete_id'], user=user).delete()
        return redirect('schedule_course')

    form = ScheduleEntryForm(request.POST or None, user=user)
    if request.method == 'POST' and 'add' in request.POST:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = user
            entry.schedule_type = ScheduleEntry.ScheduleType.COURSE
            entry.save()
            return redirect('schedule_course')

    all_entries = list(ScheduleEntry.objects.filter(user=user, schedule_type=ScheduleEntry.ScheduleType.COURSE))
    rows = build_schedule_table(all_entries, day_values)

    context = {
        'form': form,
        'rows': rows,
        'days': list(ScheduleEntry.Day),
        'all_entries': all_entries,
        'schedule_name': 'del Curso',
        'readonly': False,
        'user_role': user.role,
    }

    return render(request, 'core/schedule_personal.html', context)
