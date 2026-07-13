## habits/

| Archivo | Función |
|---------|---------|
| `models.py` | Modelos `Habit` (hábito diario con nivel que sube al completarse) y `HabitCompletion` (registro diario, unique_together habit+date) |
| `services.py` | Lógica de negocio: toggle hábito (get_or_create + incremento de nivel), crear, eliminar |
| `views/habits.py` | Vistas CRUD (solo STAFF): lista con anotaciones en 1 query (N+1 fix), toggle POST-only, crear, eliminar |
| `admin.py` | Registro de Habit y HabitCompletion en panel de administración |
| `apps.py` | Configuración de la app habits |
| `urls.py` | Rutas: listar, crear, toggle, eliminar |
