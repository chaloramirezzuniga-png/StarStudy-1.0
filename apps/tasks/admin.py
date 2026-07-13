"""Admin de tasks: registro de Task y Comment en panel de administración."""
from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'importance', 'deadline', 'assigned_to', 'assigned_by', 'is_completed']
    list_filter = ['importance', 'is_completed', 'assigned_by__role']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'created_at']
