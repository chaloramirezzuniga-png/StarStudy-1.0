from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm
from .habit_scheduler import start as start_habit_scheduler

start_habit_scheduler()

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/personal/', views.task_personal, name='task_personal'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('profile/', views.profile, name='profile'),
    path('schedule/', views.schedule_personal, name='schedule_personal'),
    path('schedule/course/', views.schedule_course, name='schedule_course'),
    path('schedule/student/course/', views.schedule_student_course, name='schedule_student_course'),
    path('join/<str:code>/', views.join, name='join'),
    path('github/connect/', views.github_connect, name='github_connect'),
    path('github/disconnect/', views.github_disconnect, name='github_disconnect'),
    path('notificaciones/', views.notification_list, name='notification_list'),
    path('notificaciones/<int:pk>/leer/', views.notification_read, name='notification_read'),
    path('habitos/', views.habito_list, name='habito_list'),
    path('habitos/crear/', views.habito_create, name='habito_create'),
    path('habitos/<int:pk>/toggle/', views.habito_toggle, name='habito_toggle'),
    path('habitos/<int:pk>/eliminar/', views.habito_delete, name='habito_delete'),
]
