"""Configuración de la app schedule: inicia APScheduler al arrancar el servidor."""
import sys
from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.schedule'
    label = 'schedule'

    def ready(self):
        if 'runserver' in sys.argv:
            from .scheduler import start
            start()
