import secrets
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
            while User.objects.filter(code=self.code).exists():
                self.code = generate_code()
        super().save(*args, **kwargs)

    def unread_notifications_count(self):
        return self.notifications.filter(is_read=False).count()

    def __str__(self):
        return f"{self.get_full_name() or self.email} ({self.get_role_display()})"


class Notification(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.message[:50]}"
