from django.contrib import admin
from .models import ScheduleEntry


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'day', 'start_time', 'end_time', 'entry_type', 'schedule_type']
