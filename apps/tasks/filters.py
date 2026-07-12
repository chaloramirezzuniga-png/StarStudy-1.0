from django.db.models import Q
from apps.tasks.models import Task


def filter_tasks(queryset, params):
    q = Q()

    importance = params.get('importance')
    if importance:
        q &= Q(importance=importance)

    status = params.get('status')
    if status == 'pending':
        q &= Q(is_completed=False)
    elif status == 'completed':
        q &= Q(is_completed=True)

    search = params.get('search')
    if search:
        q &= Q(title__icontains=search) | Q(description__icontains=search)

    if q:
        queryset = queryset.filter(q)

    return queryset
