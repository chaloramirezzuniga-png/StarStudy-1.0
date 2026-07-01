from django.contrib import admin
from .models import User, Task, ScheduleEntry, Notification, Comment, Habit, HabitCompletion


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'first_name', 'last_name', 'is_active']
    list_filter = ['role', 'is_active']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'importance', 'deadline', 'assigned_to', 'assigned_by', 'is_completed']
    list_filter = ['importance', 'is_completed', 'assigned_by__role']


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'day', 'start_time', 'end_time', 'entry_type', 'schedule_type']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'created_at']


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'level', 'created_at']


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'completed_at']
