from django.core.cache import cache

TIMEOUTS = {'unread': 120, 'home': 300, 'profile': 300, 'schedule': 1800}


def _get(key, timeout, fetch_fn):
    val = cache.get(key)
    if val is None:
        val = fetch_fn()
        cache.set(key, val, timeout)
    return val


def _invalidate(key):
    cache.delete(key)


def get_unread_count(user):
    return _get(f'unread_{user.pk}', TIMEOUTS['unread'],
                lambda: user.notifications.filter(is_read=False).count())

def invalidate_unread(user):
    _invalidate(f'unread_{user.pk}')

def get_home_stats(user_id, fetch_fn):
    return _get(f'home_{user_id}', TIMEOUTS['home'], fetch_fn)

def invalidate_home(user_id):
    _invalidate(f'home_{user_id}')

def get_profile_stats(user_id, fetch_fn):
    return _get(f'profile_{user_id}', TIMEOUTS['profile'], fetch_fn)

def invalidate_profile(user_id):
    _invalidate(f'profile_{user_id}')

def get_course_schedule(teacher_id, fetch_fn):
    return _get(f'schedule_{teacher_id}', TIMEOUTS['schedule'], fetch_fn)

def invalidate_course_schedule(teacher_id):
    _invalidate(f'schedule_{teacher_id}')
