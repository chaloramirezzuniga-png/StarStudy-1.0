from django import forms
from .models import ScheduleEntry
from apps.accounts.models import User


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
