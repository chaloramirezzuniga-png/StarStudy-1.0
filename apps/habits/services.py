from django.utils import timezone
from apps.habits.models import Habit, HabitCompletion


def toggle_habit(habit):
    today = timezone.now().date()
    _, created = HabitCompletion.objects.get_or_create(
        habit=habit,
        date=today,
    )
    if not created:
        return False, habit

    habit.level += 1
    habit.save(update_fields=['level'])
    return True, habit


def create_habit(user, title, start_time, end_time):
    return Habit.objects.create(
        user=user,
        title=title,
        start_time=start_time,
        end_time=end_time,
    )


def delete_habit(habit):
    title = habit.title
    habit.delete()
    return title
