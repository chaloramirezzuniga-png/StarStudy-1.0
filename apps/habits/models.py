from datetime import date
from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
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
    date = models.DateField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['habit', 'date']

    def __str__(self):
        return f"{self.habit.title} - {self.date}"
