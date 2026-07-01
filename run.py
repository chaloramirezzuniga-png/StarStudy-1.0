import sys, os, webbrowser, threading

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
from django.core.management import call_command
django.setup()

print(">>> Ejecutando migraciones...")
call_command('migrate', verbosity=0)

url = 'http://127.0.0.1:8000'
print(f">>> Abriendo {url} ...")
threading.Timer(1.5, lambda: webbrowser.open(url)).start()

print(f">>> Iniciando servidor en {url}")
call_command('runserver', '0.0.0.0:8000')
