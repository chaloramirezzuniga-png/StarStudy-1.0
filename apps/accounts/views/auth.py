from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.urls import reverse
from django.db import IntegrityError
from apps.accounts.models import User
from apps.accounts.forms import RegisterForm


def logout_view(request):
    auth_logout(request)
    return redirect('login')


def register(request):
    initial_code = request.GET.get('code', '').strip().upper()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                code = form.cleaned_data.get('code', '').strip().upper()
                if code and user.role == User.Role.STUDENT:
                    teacher = User.objects.filter(code=code).exclude(role=User.Role.STUDENT).first()
                    if teacher:
                        user.linked_to = teacher
                        user.save(update_fields=['linked_to'])
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Error al registrar. Intentalo de nuevo.')
    else:
        form = RegisterForm(initial={'code': initial_code})

    return render(request, 'accounts/register.html', {'form': form})


def join(request, code):
    code_upper = code.upper()
    teacher = User.objects.filter(code=code_upper).exclude(role=User.Role.STUDENT).first()
    if not teacher:
        messages.error(request, 'Código inválido o expirado')
        return redirect('register')
    return redirect(reverse('register') + '?code=' + code_upper)
