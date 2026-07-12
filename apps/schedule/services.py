from apps.schedule.models import ScheduleEntry
from apps.schedule.utils import build_schedule_table
from apps.accounts.cache import get_course_schedule, invalidate_course_schedule


def get_schedule_context(user, schedule_type, schedule_name, readonly=False):
    day_values = [d.value for d in ScheduleEntry.Day]

    if readonly and schedule_type == ScheduleEntry.ScheduleType.COURSE:
        teacher = user.linked_to
        if teacher:
            data = get_course_schedule(teacher.pk, lambda: _fetch_schedule(teacher, day_values))
            context = data.copy()
            context.update({
                'schedule_name': schedule_name,
                'readonly': readonly,
                'user_role': user.role,
            })
            return context

    all_entries = list(
        ScheduleEntry.objects.filter(user=user, schedule_type=schedule_type)
    )
    rows = build_schedule_table(all_entries, day_values)

    return {
        'rows': rows,
        'days': list(ScheduleEntry.Day),
        'all_entries': all_entries,
        'schedule_name': schedule_name,
        'readonly': readonly,
        'user_role': user.role,
    }


def _fetch_schedule(user, day_values):
    all_entries = list(
        ScheduleEntry.objects.filter(user=user, schedule_type=ScheduleEntry.ScheduleType.COURSE)
    )
    rows = build_schedule_table(all_entries, day_values)
    return {
        'rows': rows,
        'days': list(ScheduleEntry.Day),
        'all_entries': all_entries,
    }


def add_schedule_entry(user, form, schedule_type):
    entry = form.save(commit=False)
    entry.user = user
    entry.schedule_type = schedule_type
    entry.save()
    if schedule_type == ScheduleEntry.ScheduleType.COURSE:
        invalidate_course_schedule(user.pk)
    return entry


def delete_schedule_entry(entry_id, user):
    ScheduleEntry.objects.filter(pk=entry_id, user=user).delete()
    if ScheduleEntry.objects.filter(user=user, schedule_type=ScheduleEntry.ScheduleType.COURSE).exists() or True:
        invalidate_course_schedule(user.pk)
