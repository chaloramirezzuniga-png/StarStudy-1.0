import secrets
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_code():
    return secrets.token_hex(3).upper()


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Estudiante'
        TEACHER = 'TEACHER', 'Profesor'
        STAFF = 'STAFF', 'Personal'
        PROGRAMMER = 'PROGRAMMER', 'Programador'

    email = models.EmailField()
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    linked_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_students')
    github_username = models.CharField(max_length=100, blank=True, null=True)
    github_token = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def save(self, *args, **kwargs):
        if not self.code and self.role != self.Role.STUDENT:
            self.code = generate_code()
        super().save(*args, **kwargs)

    def unread_notifications_count(self):
        return self.notifications.filter(is_read=False).count()

    def __str__(self):
        return f"{self.get_full_name() or self.email} ({self.get_role_display()})"


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_entries')
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
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_tasks')
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


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.message[:50]}"


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=200)
    start_time = models.TimeField(default='00:00')
    end_time = models.TimeField(default='00:00')
    level = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-level', 'title']

    def completed_today(self):
        return self.completions.filter(date=date.today()).exists()

    def total_completions(self):
        return self.completions.count()

    def __str__(self):
        return f"{self.title} (nivel {self.level})"


class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['habit', 'date']

    def __str__(self):
        return f"{self.habit.title} - {self.date}"


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.email} - {self.text[:50]}"
