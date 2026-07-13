## accounts/

| Archivo | Función |
|---------|---------|
| `models.py` | Modelos `User` (roles, vinculación, GitHub token encriptado con Fernet) y `Notification` (alertas del sistema con cache de no leídas) |
| `cache.py` | Sistema de cache centralizado con LocMemCache. Genérico `_get()`/`_invalidate()`. Cachés: unread (2 min), home (5 min), profile (5 min), schedule (30 min) |
| `services.py` | Lógica de negocio: estadísticas de perfil con cache, vinculación profesor-estudiante por código, conexión GitHub, marcar notificaciones leídas |
| `signals.py` | Señal `post_save` en User: envía notificación de bienvenida y invalida cache de no leídas al crear usuario |
| `backends.py` | Backend de autenticación personalizado `EmailRoleBackend`: permite login por email + rol (un mismo email con múltiples roles) |
| `decorators.py` | Decoradores de control de acceso: `role_required`, `teacher_required`, `programmer_required`, `can_assign_required` |
| `forms.py` | Formularios `RegisterForm` (registro con código de vinculación) y `CustomLoginForm` (login con email + rol + contraseña) |
| `admin.py` | Registro de User y Notification en panel de administración de Django |
| `apps.py` | Configuración de la app: importa signals de bienvenida en `ready()` |
| `urls.py` | Rutas: home, register, login, logout, profile, GitHub connect/disconnect, notificaciones, join |
| `views/auth.py` | Vistas de autenticación: registro, login, logout, join por código |
| `views/home.py` | Dashboard principal: estadísticas (pendientes, vencidas, personales), sistema de nivel/xp (5 tareas = 1 nivel) |
| `views/profile.py` | Perfil de usuario: stats, vinculación, GitHub, lista de notificaciones paginada, marcar como leída (POST-only) |
