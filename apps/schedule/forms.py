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
        self._user = user
        super().__init__(*args, **kwargs)
        if user and user.role != User.Role.TEACHER:
            self.fields.pop('schedule_type')
        if user and user.role == User.Role.PROGRAMMER:
            self.fields['entry_type'].choices = [
                ('SUBJECT', 'Materia'),
                ('BREAK', 'Descanso'),
                ('LUNCH', 'Comida'),
            ]

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')
        day = cleaned_data.get('day')
        schedule_type = cleaned_data.get('schedule_type')
        if start_time and end_time and day and self._user:
            filter_kwargs = {
                'user': self._user,
                'day': day,
                'start_time__lt': end_time,
                'end_time__gt': start_time,
            }
            if schedule_type:
                filter_kwargs['schedule_type'] = schedule_type
            overlaps = ScheduleEntry.objects.filter(**filter_kwargs)
            if self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)
            if overlaps.exists():
                raise forms.ValidationError('Este horario se superpone con otro existente.')
        return cleaned_data
