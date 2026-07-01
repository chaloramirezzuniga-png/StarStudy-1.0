from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.base.models import User, Task, ScheduleEntry, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}))
    role = forms.ChoiceField(choices=User.Role.choices, label='Rol',
                             widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_role'}))
    first_name = forms.CharField(required=True, label='Nombre',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan'}))
    last_name = forms.CharField(required=True, label='Apellido',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez'}))
    code = forms.CharField(required=False, label='Código del profesor (opcional)',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A1B2C3', 'id': 'id_code'}))

    class Meta:
        model = User
        fields = ['email', 'role', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repetí la contraseña'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        role = cleaned_data.get('role')
        if email and role:
            if User.objects.filter(email=email, role=role).exists():
                raise forms.ValidationError('Ya existe un usuario con ese correo y rol.')
            if User.objects.filter(email=email, role=User.Role.STUDENT).exists() and role == User.Role.TEACHER:
                raise forms.ValidationError('No podés registrarte como Profesor con un correo que ya usaste como Estudiante.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        base = self.cleaned_data['email'].split('@')[0]
        role = self.cleaned_data.get('role', '')
        username = base + '_' + role.lower()
        counter = 1
        user.username = username
        while User.objects.filter(username=user.username).exists():
            user.username = username + '_' + str(counter)
            counter += 1
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico',
                                widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}))
    role = forms.ChoiceField(choices=User.Role.choices, label='Rol',
                             widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})
        self.fields['role'].required = True

    def clean(self):
        role = self.cleaned_data.get('role')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password and role:
            self.user_cache = authenticate(
                request=self.request,
                username=username,
                password=password,
                role=role,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Correo, rol o contraseña incorrectos.',
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ScheduleEntryForm(forms.ModelForm):
    class Meta:
        model = ScheduleEntry
        fields = ['day', 'start_time', 'end_time', 'title', 'entry_type', 'schedule_type']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Matemáticas'}),
            'entry_type': forms.Select(attrs={'class': 'form-select'}),
            'schedule_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role != User.Role.TEACHER:
            self.fields.pop('schedule_type')
        if user and user.role == User.Role.PROGRAMMER:
            self.fields['entry_type'].choices = [
                ('SUBJECT', 'Materia'),
                ('BREAK', 'Descanso'),
                ('LUNCH', 'Comida'),
            ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'importance', 'deadline', 'assigned_to', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'importance': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['deadline'].input_formats = ['%Y-%m-%dT%H:%M']
        if user and user.role != User.Role.STUDENT:
            self.fields['assigned_to'].queryset = User.objects.exclude(role=user.role)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Escribí un comentario...'}),
        }
