from django.contrib import admin
from .models import User, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'first_name', 'last_name', 'is_active']
    list_filter = ['role', 'is_active']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
