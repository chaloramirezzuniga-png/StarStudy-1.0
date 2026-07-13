"""URLs de schedule: personal, curso profesor, curso estudiante."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_personal, name='schedule_personal'),
    path('course/', views.schedule_course, name='schedule_course'),
    path('student/course/', views.schedule_student_course, name='schedule_student_course'),
]
