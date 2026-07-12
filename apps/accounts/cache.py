from django.core.cache import cache


def _key(name, user_id):
    return f'{name}_{user_id}'


TIMEOUTS = {
    'unread': 120,
    'home': 300,
    'profile': 300,
    'schedule': 1800,
}


def get_unread_count(user):
    k = _key('unread', user.pk)
    count = cache.get(k)
    if count is None:
        count = user.notifications.filter(is_read=False).count()
        cache.set(k, count, TIMEOUTS['unread'])
    return count


def invalidate_unread(user):
    cache.delete(_key('unread', user.pk))


def get_home_stats(user_id, fetch_fn):
    k = _key('home', user_id)
    stats = cache.get(k)
    if stats is None:
        stats = fetch_fn()
        cache.set(k, stats, TIMEOUTS['home'])
    return stats


def invalidate_home(user_id):
    cache.delete(_key('home', user_id))


def get_profile_stats(user_id, fetch_fn):
    k = _key('profile', user_id)
    stats = cache.get(k)
    if stats is None:
        stats = fetch_fn()
        cache.set(k, stats, TIMEOUTS['profile'])
    return stats


def invalidate_profile(user_id):
    cache.delete(_key('profile', user_id))


def get_course_schedule(teacher_id, fetch_fn):
    k = _key('schedule', teacher_id)
    data = cache.get(k)
    if data is None:
        data = fetch_fn()
        cache.set(k, data, TIMEOUTS['schedule'])
    return data


def invalidate_course_schedule(teacher_id):
    cache.delete(_key('schedule', teacher_id))
