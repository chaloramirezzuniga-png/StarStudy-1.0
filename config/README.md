## config/

| Archivo | Función |
|---------|---------|
| `settings.py` | Configuración de Django: SQLite (timeout 20s), LocMemCache, autenticación por email+rol, zona horaria Argentina, seguridad (HSTS, XSS, CSRF, X-Frame-Options), 4 apps instaladas |
| `urls.py` | URLs principales: admin, accounts, tasks, habits, schedule. Sirve archivos media en desarrollo |
| `wsgi.py` | Punto de entrada WSGI para despliegue en producción |
| `asgi.py` | Punto de entrada ASGI para despliegue en producción |
