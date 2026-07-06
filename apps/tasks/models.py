from django.conf import settings
from django.db import models


class Task(models.Model):
    class Importance(models.TextChoices):
        LOW = 'LOW', 'Baja'
        MEDIUM = 'MEDIUM', 'Media'
        HIGH = 'HIGH', 'Alta'
        CRITICAL = 'CRITICAL', 'Crítica'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    importance = models.CharField(max_length=20, choices=Importance.choices, default=Importance.MEDIUM)
    deadline = models.DateTimeField()
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_tasks')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_personal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='task_files/', blank=True, null=True)

    class Meta:
        ordering = ['-importance', 'deadline']

    def __str__(self):
        return f"{self.title} - {self.assigned_to.email}"


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.email} - {self.text[:50]}"
