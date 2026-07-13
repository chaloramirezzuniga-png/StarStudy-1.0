"""Decoradores de control de acceso por rol.

- role_required(*roles): requiere login + rol específico.
- teacher_required: atajo para role_required('TEACHER').
- programmer_required: atajo para role_required('PROGRAMMER').
- can_assign_required: requiere TEACHER, STAFF o PROGRAMMER.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in roles:
                messages.error(request, 'No tenés permiso para acceder a esta página.')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def teacher_required(view_func):
    return role_required('TEACHER')(view_func)


def programmer_required(view_func):
    return role_required('PROGRAMMER')(view_func)


def can_assign_required(view_func):
    return role_required('TEACHER', 'STAFF', 'PROGRAMMER')(view_func)
