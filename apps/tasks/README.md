## tasks/

| Archivo | Función |
|---------|---------|
| `models.py` | Modelos `Task` (importancia, deadline, asignación bidireccional, is_personal, 3 índices compuestos) y `Comment` (comentarios en tareas) |
| `services.py` | Lógica de negocio: queryset optimizado por rol, filtros de importancia/estado, crear/completar/eliminar tareas, invalidación de caches |
| `signals.py` | Señal `post_save` en Task: notifica al asignado cuando se crea una tarea no personal por otro usuario |
| `forms.py` | Formularios `TaskForm` (asigna a estudiantes si eres profesor, archivo adjunto) y `CommentForm` (textarea de comentarios) |
| `views/tasks.py` | Vistas: lista unificada (asignadas + personales), detalle con comentarios, crear, completar, eliminar, comentar |
| `admin.py` | Registro de Task y Comment en panel de administración |
| `apps.py` | Configuración de la app: importa signals de notificación en `ready()` |
| `urls.py` | Rutas: lista, personal, crear, detalle, completar, eliminar, comentar |
