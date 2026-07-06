from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.habits.models import Habit, HabitCompletion


@login_required
def habito_list(request):
    if request.user.role != 'STAFF':
        messages.error(request, 'No tenés acceso a esta sección.')
        return redirect('home')
    habits = request.user.habits.all()
    return render(request, 'habits/habito_list.html', {'habits': habits})


@login_required
def habito_toggle(request, pk):
    if request.user.role != 'STAFF':
        messages.error(request, 'No tenés acceso.')
        return redirect('home')
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    from datetime import date
    completion, created = HabitCompletion.objects.get_or_create(
        habit=habit,
        date=date.today()
    )
    if not created:
        messages.error(request, f'No podés desmarcar "{habit.title}" hasta mañana.')
    else:
        habit.level += 1
        habit.save(update_fields=['level'])
        messages.success(request, f'"{habit.title}" completado. ¡Subiste al nivel {habit.level}!')
    return redirect('habito_list')


@login_required
def habito_create(request):
    if request.user.role != 'STAFF':
        messages.error(request, 'No tenés acceso.')
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        start_time = request.POST.get('start_time', '').strip()
        end_time = request.POST.get('end_time', '').strip()
        if title and start_time and end_time:
            Habit.objects.create(user=request.user, title=title, start_time=start_time, end_time=end_time)
            messages.success(request, f'Hábito "{title}" creado.')
            return redirect('habito_list')
        else:
            messages.error(request, 'Completá todos los campos.')
    return render(request, 'habits/habito_form.html')


@login_required
def habito_delete(request, pk):
    if request.user.role != 'STAFF':
        messages.error(request, 'No tenés acceso.')
        return redirect('home')
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    title = habit.title
    habit.delete()
    messages.success(request, f'Hábito "{title}" eliminado.')
    return redirect('habito_list')
