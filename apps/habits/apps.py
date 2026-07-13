"""Configuración de la app habits: gestión de hábitos diarios."""
from django.apps import AppConfig


class HabitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.habits'
    label = 'habits'
