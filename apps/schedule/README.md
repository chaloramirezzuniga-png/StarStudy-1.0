## schedule/

| Archivo | Función |
|---------|---------|
| `models.py` | Modelo `ScheduleEntry` (día Lun-Vie, hora inicio/fin, título, tipo: Materia/Recreo/Almuerzo, horario: Personal/Curso) |
| `services.py` | Lógica de negocio: contexto del horario con cache (30 min para cursos), crear/eliminar entradas e invalidar cache |
| `scheduler.py` | APScheduler en background: verifica hábitos (±2 min ventana) y deadlines de tareas cada 1 min, crea notificaciones |
| `forms.py` | Formulario de entrada horaria: valida hora fin > inicio, sin superposición, entry_type limitado para PROGRAMMER |
| `utils.py` | Construcción de la grilla: `build_schedule_table()` genera filas (hora × día) desde las entradas del horario |
| `views/schedule.py` | Vistas: schedule personal (r/w), schedule curso profesor (r/w, solo TEACHER), schedule curso estudiante (solo lectura, solo STUDENT) |
| `admin.py` | Registro de ScheduleEntry en panel de administración |
| `apps.py` | Configuración de la app: inicia APScheduler al arrancar el servidor con `runserver` |
| `urls.py` | Rutas: personal, curso profesor, curso estudiante |
