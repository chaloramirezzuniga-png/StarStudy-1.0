from django.urls import path
from . import views
from .scheduler import start as start_habit_scheduler

start_habit_scheduler()

urlpatterns = [
    path('', views.schedule_personal, name='schedule_personal'),
    path('course/', views.schedule_course, name='schedule_course'),
    path('student/course/', views.schedule_student_course, name='schedule_student_course'),
]
