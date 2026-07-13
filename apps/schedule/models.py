"""Models de schedule: Entrada de horario.

- ScheduleEntry: entrada horaria con día (Lun-Vie), hora inicio/fin, título,
  tipo de entrada (Materia/Recreo/Almuerzo) y tipo de horario (Personal/Curso).
  El schedule_type se asigna automáticamente en la vista (no en el formulario).
"""
from django.conf import settings
from django.db import models


class ScheduleEntry(models.Model):
    class Day(models.TextChoices):
        MONDAY = 'MON', 'Lunes'
        TUESDAY = 'TUE', 'Martes'
        WEDNESDAY = 'WED', 'Miércoles'
        THURSDAY = 'THU', 'Jueves'
        FRIDAY = 'FRI', 'Viernes'

    class EntryType(models.TextChoices):
        SUBJECT = 'SUBJECT', 'Materia'
        BREAK = 'BREAK', 'Recreo'
        LUNCH = 'LUNCH', 'Almuerzo'

    class ScheduleType(models.TextChoices):
        PERSONAL = 'PERSONAL', 'Personal'
        COURSE = 'COURSE', 'Curso'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='schedule_entries')
    day = models.CharField(max_length=3, choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    title = models.CharField(max_length=200)
    entry_type = models.CharField(max_length=10, choices=EntryType.choices, default=EntryType.SUBJECT)
    schedule_type = models.CharField(max_length=10, choices=ScheduleType.choices, default=ScheduleType.PERSONAL)

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time}-{self.end_time} {self.title}"
