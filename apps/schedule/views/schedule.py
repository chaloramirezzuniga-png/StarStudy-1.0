from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.schedule.models import ScheduleEntry
from apps.schedule.forms import ScheduleEntryForm
from apps.schedule.services import get_schedule_context, add_schedule_entry, delete_schedule_entry
from apps.accounts.decorators import role_required


@login_required
def schedule_personal(request):
    user = request.user

    if request.method == 'POST' and 'delete_id' in request.POST:
        delete_schedule_entry(request.POST['delete_id'], user)
        return redirect('schedule_personal')

    form = ScheduleEntryForm(request.POST or None, user=user)
    if request.method == 'POST' and 'add' in request.POST and form.is_valid():
        add_schedule_entry(user, form, ScheduleEntry.ScheduleType.PERSONAL)
        return redirect('schedule_personal')

    context = get_schedule_context(user, ScheduleEntry.ScheduleType.PERSONAL, 'Personal')
    context['form'] = form
    return render(request, 'schedule/schedule_personal.html', context)


@login_required
def schedule_student_course(request):
    teacher = request.user.linked_to
    if not teacher:
        messages.error(request, 'No estás vinculado a ningún profesor.')
        return redirect('schedule_personal')

    context = get_schedule_context(teacher, ScheduleEntry.ScheduleType.COURSE, 'del Curso', readonly=True)
    return render(request, 'schedule/schedule_personal.html', context)


@role_required('TEACHER')
def schedule_course(request):
    user = request.user

    if request.method == 'POST' and 'delete_id' in request.POST:
        delete_schedule_entry(request.POST['delete_id'], user)
        return redirect('schedule_course')

    form = ScheduleEntryForm(request.POST or None, user=user)
    if request.method == 'POST' and 'add' in request.POST and form.is_valid():
        add_schedule_entry(user, form, ScheduleEntry.ScheduleType.COURSE)
        return redirect('schedule_course')

    context = get_schedule_context(user, ScheduleEntry.ScheduleType.COURSE, 'del Curso')
    context['form'] = form
    return render(request, 'schedule/schedule_personal.html', context)
