# Descripción Informática - StarStudy 1.0

> Guía completa de cada archivo del proyecto, explicada para alguien que está empezando a programar.
> Cada archivo se describe como si fuera una pieza de un rompecabezas: qué hace, por qué existe y cómo se conecta con el resto.

---

## Tabla de Contenidos

1. [¿Qué es Django?](#qué-es-django)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Archivos de configuración (config/)](#archivos-de-configuración)
4. [App: accounts (cuentas de usuario)](#app-accounts)
5. [App: tasks (tareas)](#app-tasks)
6. [App: habits (hábitos)](#app-habits)
7. [App: schedule (horarios)](#app-schedule)

---

## ¿Qué es Django?

**Django** es un framework web en Python. Piensa en él como un **constructor de edificios**: en vez de construir cada ladrillo desde cero, Django te da paredes, puertas y ventanas prefabricadas. Vos solo tenés que decidir cómo distribuirlas.

Un **framework** es como un kit de herramientas que ya viene armado. En vez de escribir todo el código para que una página web funcione (base de datos, usuario, login, etc.), Django ya lo hizo por vos. Vos solo conectás las piezas.

### Conceptos básicos

| Concepto | Analogía | Ejemplo en el proyecto |
|----------|----------|----------------------|
| **Model** | El plano de una casa (define qué datos guardás) | `User`, `Task`, `Habit` |
| **View** | El electricista que conecta todo (recibe petición, devuelve respuesta) | `home()`, `task_list()` |
| **Template** | La fachada de la casa (lo que ve el usuario en pantalla) | `home.html`, `base.html` |
| **URL** | La dirección de la casa (a dónde vas para llegar a cada página) | `/tasks/`, `/profile/` |
| **Form** | El formulario de inscripción (valida que los datos estén bien) | `TaskForm`, `RegisterForm` |
| **Signal** | Una alarma automática (se dispara cuando pasa algo) | Bienvenida al registrarse |
| **Cache** | Un cuaderno de notas rápido (guardás datos para no volver a calcularlos) | Estadísticas del home |
| **Migration** | La receta para crear la base de datos (define las tablas) | `0001_initial.py` |

---

## Estructura del proyecto

```
StarStudy-1.0/
├── config/                  ← Configuración del edificio
│   ├── settings.py          ← El interruptor principal
│   ├── urls.py              ← El directorio de direcciones
│   ├── wsgi.py              ← La puerta de entrada (producción)
│   └── asgi.py              ← La puerta alternativa (producción)
├── apps/                    ← Las habitaciones del edificio
│   ├── accounts/            ← La recepción (quién entró)
│   ├── tasks/               ← La sala de tareas
│   ├── habits/              ← El cuaderno de hábitos
│   └── schedule/            ← El calendario
├── static/                  ← Los muebles y decoraciones (CSS, imágenes)
├── templates/               ← Las plantillas de las páginas web
└── manage.py                ← El control remoto del proyecto
```

---

## Archivos de configuración

### `manage.py`

**¿Qué es?** Es el control remoto del proyecto. Desde la terminal, escribís comandos como `python manage.py runserver` para encender el servidor, o `python manage.py migrate` para crear las tablas de la base de datos.

**Analogía:** Es como el mando a distancia de tu tele. Sin él, no podés cambiar de canal ni subir el volumen.

**Importancia:** Sin este archivo no podés ejecutar nada del proyecto. Es el punto de partida.

---

### `config/settings.py`

**¿Qué es?** Es el archivo de configuración más importante. Aquí se define TODO:
- Qué aplicaciones tiene el proyecto
- Qué base de datos se usa (SQLite en nuestro caso)
- La zona horaria (Argentina)
- Las reglas de seguridad (contraseñas, cookies)
- Dónde buscar archivos estáticos y plantillas
- Dónde guardar imágenes subidas por los usuarios

**Analogía:** Es como el manual de instrucciones de una casa. Dice cuántos pisos tiene, dónde está la llave del gas, y qué hora hay en el reloj.

**Configuraciones clave en nuestro proyecto:**
```python
AUTH_USER_MODEL = 'accounts.User'  # Usa nuestro modelo de usuario personalizado
AUTHENTICATION_BACKENDS = ['apps.accounts.backends.EmailRoleBackend']  # Login por email + rol
CACHES = { ... }  # Sistema de caché para hacer las cosas más rápidas
TIME_ZONE = 'America/Argentina/Buenos_Aires'  # Hora de Argentina
```

**Importancia:** Si algo está mal acá, todo el proyecto falla. Es como tener la dirección de tu casa mal escrita: nadie te va a encontrar.

---

### `config/urls.py`

**¿Qué es?** Es el mapa de direcciones del sitio. Cada página tiene una "dirección" (URL), y este archivo dice a qué "habitación" (vista) ir cuando alguien visita esa dirección.

**Analogía:** Es como el directorio telefónico. Cuando marcás un número, el operador te conecta con la persona correcta.

```python
urlpatterns = [
    path('admin/', admin.site.urls),        # /admin/ → Panel de administración
    path('', include('apps.accounts.urls')),# / → Páginas de accounts
    path('tasks/', include('apps.tasks.urls')),# /tasks/ → Páginas de tareas
    path('habitos/', include('apps.habits.urls')),# /habitos/ → Páginas de hábitos
    path('schedule/', include('apps.schedule.urls')),# /schedule/ → Páginas de horarios
]
```

**Importancia:** Sin esto, cuando alguien escribe tu página web, no sabría a dónde ir. Es como una casa sin número: nadie te encuentra.

---

### `config/wsgi.py` y `config/asgi.py`

**¿Qué son?** Son los puntos de entrada para cuando el sitio está en producción (internet real). WSGI es para peticiones normales, ASGI para peticiones en tiempo real (como websockets).

**Analogía:** WSGI es la puerta principal de un edificio, ASGI es la puerta de emergencia. Ambas sirven para entrar, pero la ASGI puede manejar cosas más rápidas.

**Importancia:** Solo los usás cuando subís el sitio a internet. En desarrollo (cuando estás probando en tu computadora), no los necesitás.

---

## App: accounts

> Esta app es la **recepción del edificio**: maneja quién es cada usuario, quién tiene permiso para qué, y las notificaciones.

### `apps/accounts/models.py`

**¿Qué es?** Define las **tablas de la base de datos**. Cada clase es una tabla.

**Analogía:** Es como el formulario de inscripción de un club. Define qué datos se guardan de cada socio: nombre, email, rol, etc.

**Qué guarda:**

#### Modelo `User` (Usuario)
```python
class User(AbstractUser):
    email = models.EmailField()           # Email del usuario
    role = models.CharField(...)          # Rol: STUDENT, TEACHER, STAFF, PROGRAMMER
    code = models.CharField(...)          # Código para vincular profesor-estudiante
    linked_to = models.ForeignKey(...)    # A qué profesor está vinculado
    github_username = models.CharField(...) # Usuario de GitHub (solo programadores)
    github_token = models.TextField(...)  # Token de GitHub encriptado (contraseña)
```

**Métodos importantes:**
- `set_github_token(raw_token)`: Encripta y guarda el token de GitHub. Es como meter una carta en un sobre cerrado antes de guardarla.
- `get_github_token()`: Saca la carta del sobre y la lee.
- `unread_notifications_count()`: Cuenta cuántas notificaciones sin leer tenés (con caché).

#### Modelo `Notification` (Notificación)
```python
class Notification(models.Model):
    user = models.ForeignKey(User, ...)   # A quién le llega
    message = models.CharField(...)       # Qué dice
    link = models.CharField(...)          # A dónde te lleva al hacer clic
    is_read = models.BooleanField(...)    # ¿Ya la viste?
    created_at = models.DateTimeField(...)# Cuándo llegó
```

**Importancia:** Sin modelos no hay base de datos. Sin base de datos no hay datos. Sin datos, la página estaría vacía.

---

### `apps/accounts/cache.py`

**¿Qué es?** Es el sistema de **caché**. Caché es como un cuaderno de notas rápido: en vez de buscar la información cada vez que alguien la necesita, la escribís en un papelito y la mirás rápido.

**Analogía:** Imaginás que tu mamá te pregunta "¿qué hora es?" cada 5 minutos. En vez de mirar el reloj cada vez, anotás la hora en un papel y le mostrás el papel. Eso es caché.

**Qué cachea:**
| Caché | Tiempo | Qué guarda |
|-------|--------|-----------|
| `unread` | 2 minutos | Cuántas notificaciones sin leer tenés |
| `home` | 5 minutos | Estadísticas del home (tareas pendientes, vencidas, etc.) |
| `profile` | 5 minutos | Estadísticas del perfil (tareas asignadas, completadas, etc.) |
| `schedule` | 30 minutos | Horario del curso del profesor |

**Funciones principales:**
- `get_unread_count(user)`: "¿Cuántas notificaciones sin leer tengo?" (guarda la respuesta 2 min)
- `invalidate_unread(user)`: "¡Se creó una notificación nueva!" (borra el papelito para calcular de nuevo)
- `get_home_stats(user_id, fetch_fn)`: "¿Cuántas tareas tengo?" (guarda la respuesta 5 min)
- `invalidate_home(user_id)`: "¡Se creó/completó una tarea!" (borra el papelito)
- `get_profile_stats(user_id, fetch_fn)`: "¿Cuántas tareas completé?" (guarda 5 min)
- `invalidate_profile(user_id)`: "¡Se completó una tarea!" (borra el papelito)
- `get_course_schedule(teacher_id, fetch_fn)`: "¿Qué horario tiene el curso?" (guarda 30 min)
- `invalidate_course_schedule(teacher_id)`: "¡Se cambió el horario!" (borra el papelito)

**Importancia:** Sin caché, cada vez que alguien visita una página, el servidor tendría que buscar TODO de nuevo. Con caché, busca una vez y guarda el resultado. Es como tener la respuesta escrita en vez de tener que calcularla cada vez.

---

### `apps/accounts/services.py`

**¿Qué es?** Contiene la **lógica de negocio**. En programación, "lógica de negocio" significa las reglas de cómo funciona tu aplicación.

**Analogía:** Es como el libro de recetas de un restaurante. Cada receta dice qué hacer paso a paso.

**Qué hace:**
- `get_user_stats(user)`: Calcula las estadísticas del perfil (tareas asignadas, completadas, pendientes) y las cachea.
- `link_student_to_teacher(user, code)`: Vincula un estudiante a un profesor usando un código de 6 caracteres.
- `connect_github(user, username)`: Conecta la cuenta de GitHub de un programador.
- `disconnect_github(user)`: Desconecta la cuenta de GitHub.
- `mark_notification_read(notification)`: Marca una notificación como leída y borra el caché de no leídas.

**Importancia:** Las vistas (views) no deberían tener lógica complicada. Los servicios separan la lógica para que el código sea más fácil de entender y mantener.

---

### `apps/accounts/signals.py`

**¿Qué es?** Son **señales automáticas**. Django tiene un sistema de "señales" que se disparan cuando pasa algo. Como una alarma automática.

**Analogía:** Es como el timbre de tu casa. Cuando alguien toca, el timbre suena automáticamente. Vos no tenés que estar mirando la puerta todo el tiempo.

**Qué hace:**
```python
@receiver(post_save, sender=User)
def notificar_bienvenida(sender, instance, created, **kwargs):
    if created:  # Si se creó un usuario nuevo...
        Notification.objects.create(...)  # ...le envía una notificación de bienvenida
        invalidate_unread(instance)       # ...y actualiza el caché de notificaciones
```

**Importancia:** Sin signals, tendrías que escribir manualmente "enviar notificación de bienvenida" en cada vista donde se crea un usuario. Con signals, Django lo hace solo.

---

### `apps/accounts/backends.py`

**¿Qué es?** Es el **backend de autenticación**. Define CÓMO se verifica que un usuario es quien dice ser.

**Analogía:** Es como el guardia de seguridad de un edificio. Cuando alguien dice "soy Juan", el guardia verifica: ¿tiene credencial? ¿Está en la lista? ¿La credencial no está vencida?

**Qué hace:**
```python
class EmailRoleBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, role=None, **kwargs):
        # Busca usuario por email Y rol
        # Si lo encuentra y la contraseña es correcta → lo deja entrar
        # Si no → lo rechaza
```

**Por qué es especial:** Permite que el mismo email tenga múltiples cuentas con diferentes roles. Por ejemplo, `juan@correo.com` puede tener una cuenta de Estudiante Y otra de Profesor.

**Importancia:** Sin esto, el login no funcionaría. Es la primera línea de defensa contra intrusos.

---

### `apps/accounts/decorators.py`

**¿Qué son?** Los **decoradores** son etiquetas que ponés encima de una función para cambiar su comportamiento. En este caso, controlan quién puede acceder a qué página.

**Analogía:** Es como los candados de diferentes habitaciones. Para entrar a la habitación del profesor, necesitás la llave del profesor. Para entrar a la de programador, la del programador.

**Qué decoradores hay:**
- `@role_required('TEACHER', 'STAFF')`: Solo pueden entrar usuarios con ese rol.
- `@teacher_required`: Atajo para `role_required('TEACHER')`.
- `@programmer_required`: Atajo para `role_required('PROGRAMMER')`.
- `@can_assign_required`: Solo pueden entrar TEACHER, STAFF o PROGRAMMER.

**Ejemplo:**
```python
@role_required('TEACHER')  # ← Solo profesores pueden ver esta página
def schedule_course(request):
    ...
```

**Importancia:** Sin decoradores, cualquier usuario podría ver cualquier página. Es como no tener cerraduras en las puertas.

---

### `apps/accounts/forms.py`

**¿Qué es?** Son los **formularios**. Definen los campos que el usuario llena (nombre, email, contraseña, etc.) y las reglas de validación.

**Analogía:** Es como el formulario de inscripción de un club. Tiene campos: "Nombre", "Email", "Contraseña". Y reglas: "El email debe tener @", "La contraseña debe tener 8 caracteres".

**Qué formularios hay:**

#### `RegisterForm` (Registro)
- Campos: email, rol, nombre, apellido, contraseña ×2, código de vinculación (opcional)
- Validaciones:
  - No podés tener dos cuentas con el mismo email Y rol
  - El código de vinculación debe ser válido (si sos estudiante)
  - Si ya tenés una cuenta con otro rol, necesitás otro email

#### `CustomLoginForm` (Login)
- Campos: email, rol, contraseña
- Validación: Verifica que email + rol + contraseña coincidan
- Usa el backend personalizado `EmailRoleBackend`

**Importancia:** Sin forms, los usuarios podrían meter basura en la base de datos (emails sin @, contraseñas de 1 letra, etc.).

---

### `apps/accounts/views/home.py`

**¿Qué es?** Es la **vista del home** (página principal). Lo primero que ve el usuario después de hacer login.

**Analogía:** Es como la sala principal de un centro de estudios. Tenés un resumen de todo: cuántas tareas tenés pendientes, cuántas vencieron, cuántas completaste, y tu nivel.

**Qué muestra:**
- **Tareas pendientes:** Las que todavía no terminaste
- **Tareas vencidas:** Las que ya pasaron de fecha
- **Tareas personales:** Las que te creaste para vos mismo
- **Nivel y XP:** Cada 5 tareas completadas subís de nivel
- **Tareas recientes:** Las últimas 5 tareas pendientes

**Cómo funciona:**
1. Llama a `get_home_stats()` que usa caché de 5 minutos
2. Calcula nivel y XP a partir de tareas completadas
3. Manda todo al template `home.html` para que se renderice

**Importancia:** Es la primera impresión del usuario. Si es lenta o confusa, el usuario no va a querer usar la app.

---

### `apps/accounts/views/profile.py`

**¿Qué es?** Son las **vistas del perfil**. Muestran información del usuario y permiten hacer acciones.

**Analogía:** Es como la ficha de un socio en el club. Mostrás sus datos, sus estadísticas, y podés hacer cosas como vincularse a un profesor o conectar GitHub.

**Qué hace cada vista:**
- `profile()`: Muestra el perfil con estadísticas. Los estudiantes pueden vincularse con un código.
- `github_connect()`: Conecta la cuenta de GitHub (solo programadores).
- `github_disconnect()`: Desconecta la cuenta de GitHub.
- `notification_list()`: Lista todas las notificaciones (paginadas, 20 por página).
- `notification_read()`: Marca una notificación como leída (solo POST, con CSRF).

**Importancia:** El perfil es donde el usuario gestiona su información. Sin estas vistas, no podría vincularse a profesores ni ver sus notificaciones.

---

### `apps/accounts/views/auth.py`

**¿Qué es?** Son las **vistas de autenticación**: registro, login y logout.

**Analogía:** Es como la recepción del club. Acá es donde te registrás (inscripción), entrás (login), o salís (logout).

**Qué hace cada vista:**
- `register()`: Formulario para crear cuenta nueva. Si el rol es Estudiante y tiene código, lo vincula automáticamente al profesor.
- `logout_view()`: Cierra la sesión del usuario y lo manda al login.
- `join(request, code)`: Recibe un código por URL (`/join/A1B2C3/`) y redirige al registro con el código prellenado.

**Importancia:** Sin estas vistas, nadie podría crear cuenta ni entrar al sistema.

---

## App: tasks

> Esta app es la **sala de tareas**: maneja todo lo relacionado con tareas asignadas entre usuarios.

### `apps/tasks/models.py`

**¿Qué es?** Define los modelos `Task` (tarea) y `Comment` (comentario).

**Qué guarda cada tarea:**
```python
class Task(models.Model):
    title = models.CharField(...)         # Título de la tarea
    description = models.TextField(...)   # Descripción detallada
    importance = models.CharField(...)    # Importancia: LOW, MEDIUM, HIGH, CRITICAL
    deadline = models.DateTimeField(...)  # Fecha límite
    assigned_by = models.ForeignKey(...)  # Quién la creó
    assigned_to = models.ForeignKey(...)  # A quién se la asignaron
    is_completed = models.BooleanField(...)# ¿Está completada?
    completed_at = models.DateTimeField(...)# Cuándo se completó
    is_personal = models.BooleanField(...)# ¿Es personal (solo para mí)?
    file = models.FileField(...)          # Archivo adjunto (opcional)
```

**Orden de las tareas:** Las tareas se ordenan automáticamente por importancia: CRITICAL → HIGH → MEDIUM → LOWN, y luego por deadline (la más urgente primero).

**Índices:** La base de datos tiene "índices" (como un índice de libro) para que las búsquedas sean más rápidas.

**Qué guarda cada comentario:**
```python
class Comment(models.Model):
    task = models.ForeignKey(Task, ...)   # En qué tarea
    user = models.ForeignKey(User, ...)   # Quién lo escribió
    text = models.TextField(...)          # Qué dijo
```

**Importancia:** Sin modelos, no hay estructura para guardar datos. Es como intentar guardar libros sin estantes: todo se pierde.

---

### `apps/tasks/services.py`

**¿Qué es?** La lógica de negocio para las tareas.

**Qué hace:**
- `get_task_queryset(user, is_personal)`: Retorna las tareas según el rol. Si sos profesor, ves las que creaste. Si sos estudiante, ves las que te asignaron.
- `apply_filters(queryset, importance, status, now)`: Filtra tareas por importancia y estado (pendiente, completada, vencida).
- `create_task(form, user, is_personal)`: Crea una tarea y invalida los caches.
- `complete_task(task, user)`: Marca una tarea como completada, envía notificación al creador, y invalida caches.
- `delete_task(task)`: Elimina una tarea (captura datos antes de borrar para invalidar caches).
- `add_comment(task, user, text)`: Agrega un comentario a una tarea.

**Importancia:** Separa la lógica de las vistas. Si mañana querés cambiar cómo se crean las tareas, solo tocás acá, no tenés que buscar entre 10 vistas.

---

### `apps/tasks/signals.py`

**¿Qué es?** Señal automática al crear tareas.

**Qué hace:** Cuando se crea una tarea que:
- No es personal (`is_personal=False`)
- Fue asignada por alguien diferente al destinatario

...se crea una notificación automática para el destinatario: "Juan te asignó: tarea X".

**Importancia:** Sin esto, el destinatario no sabría que le asignaron una tarea hasta que entre manualmente a mirar.

---

### `apps/tasks/forms.py`

**¿Qué son?** Formularios para crear tareas y comentarios.

**TaskForm:**
- Campos: título, descripción, importancia, deadline, archivo adjunto, asignado a
- Si el usuario es profesor/personal/programador, el campo "asignado a" muestra solo estudiantes
- Si el usuario es estudiante, no puede elegir a quién asignarle (se le asigna a sí mismo)

**CommentForm:**
- Un solo campo: texto del comentario

**Importancia:** Validan que los datos sean correctos antes de guardarlos en la base de datos.

---

### `apps/tasks/views/tasks.py`

**¿Qué es?** Las vistas (controladores) de las tareas.

**Qué hace cada vista:**
- `task_list()`: Lista todas las tareas con filtros y paginación (10 por página). Unificada para tareas asignadas y personales.
- `task_personal()`: Atajo a `task_list()` con `is_personal=True`.
- `task_detail()`: Muestra el detalle de una tarea con sus comentarios (paginados).
- `task_create()`: Formulario para crear una tarea (asignada o personal).
- `task_complete()`: Marca una tarea como completada (solo POST, para evitar clics accidentales).
- `task_delete()`: Elimina una tarea (solo si vos la creaste).
- `comment_create()`: Agrega un comentario a una tarea.

**Importancia:** Son las puertas de entrada. Cada vista responde a una URL diferente.

---

## App: habits

> Esta app es el **cuaderno de hábitos**: maneja los hábitos diarios de los usuarios (solo STAFF).

### `apps/habits/models.py`

**¿Qué es?** Define los modelos `Habit` (hábito) y `HabitCompletion` (registro de completación).

**Qué guarda cada hábito:**
```python
class Habit(models.Model):
    user = models.ForeignKey(User, ...)   # De quién es
    title = models.CharField(...)         # Nombre del hábito
    start_time = models.TimeField(...)    # Hora de inicio
    end_time = models.TimeField(...)      # Hora de fin
    level = models.PositiveIntegerField(...)# Nivel (sube al completar)
```

**Qué guarda cada completación:**
```python
class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, ...) # De qué hábito es
    date = models.DateField(...)          # Qué día se completó
```

**Regla:** Un hábito solo se puede completar UNA vez por día (unique_together).

**Importancia:** Sin estos modelos, no podrías trackear tus hábitos diarios.

---

### `apps/habits/services.py`

**¿Qué es?** Lógica de negocio para hábitos.

**Qué hace:**
- `toggle_habit(habit)`: Marca un hábito como completado hoy. Si ya estaba completado, no hace nada. Si se completó, sube el nivel del hábito (+1).
- `create_habit(user, title, start_time, end_time)`: Crea un hábito nuevo.
- `delete_habit(habit)`: Elimina un hábito y retorna su título para mostrar un mensaje.

**Importancia:** Separa la lógica de las vistas.

---

### `apps/habits/views/habits.py`

**¿Qué es?** Las vistas de hábitos (solo STAFF puede usarlas).

**Qué hace cada vista:**
- `habito_list()`: Lista todos tus hábitos con anotaciones: cuántas veces se completó en total y si ya se completó hoy. Todo en UNA sola consulta a la base de datos (N+1 fix).
- `habito_toggle()`: Marca/desmarca un hábito (POST-only). No permite desmarcar hasta mañana.
- `habito_create()`: Formulario para crear un hábito con título y horarios.
- `habito_delete()`: Elimina un hábito (POST-only).

**Importancia:** CRUD (Create, Read, Update, Delete) de hábitos. Sin estas vistas, no podrías gestionar tus hábitos.

---

## App: schedule

> Esta app es el **calendario de horarios**: maneja los horarios personales y de curso.

### `apps/schedule/models.py`

**¿Qué es?** Define el modelo `ScheduleEntry` (entrada de horario).

**Qué guarda:**
```python
class ScheduleEntry(models.Model):
    user = models.ForeignKey(User, ...)   # De quién es
    day = models.CharField(...)           # Día: MON, TUE, WED, THU, FRI
    start_time = models.TimeField(...)    # Hora de inicio
    end_time = models.TimeField(...)      # Hora de fin
    title = models.CharField(...)         # Nombre (ej: "Matemáticas")
    entry_type = models.CharField(...)    # Tipo: SUBJECT, BREAK, LUNCH
    schedule_type = models.CharField(...) # Tipo: PERSONAL o COURSE
```

**Tipos de entrada:**
- `SUBJECT`: Materia (clase)
- `BREAK`: Recreo
- `LUNCH`: Almuerzo

**Tipos de horario:**
- `PERSONAL`: Tu horario personal
- `COURSE`: Horario del curso del profesor

**Importancia:** Sin este modelo, no podrías guardar tus horarios.

---

### `apps/schedule/services.py`

**¿Qué es?** Lógica de negocio para horarios.

**Qué hace:**
- `get_schedule_context(user, schedule_type, schedule_name, readonly)`: Construye el contexto (datos) para renderizar el horario. Para estudiantes, usa el horario del profesor vinculado con caché de 30 minutos.
- `add_schedule_entry(user, form, schedule_type)`: Crea una entrada de horario y invalida el caché si es horario de curso.
- `delete_schedule_entry(entry_id, user)`: Elimina una entrada de horario y invalida el caché si es horario de curso.

**Importancia:** Separa la lógica y maneja el caché de horarios.

---

### `apps/schedule/scheduler.py`

**¿Qué es?** El **scheduler** (programador de tareas) que corre en background. Usa APScheduler para ejecutar tareas automáticas cada cierto tiempo.

**Analogía:** Es como un despertador que suena cada minuto y revisa si hay algo que hacer.

**Qué revisa:**

#### `check_habit_notifications()` (cada 1 minuto)
- Revisa todos los hábitos de todos los usuarios
- Si un hábito tiene hora de inicio o fin dentro de una ventana de ±2 minutos
- Y no se le envió notificación hoy
- → Crea una notificación: "¡Hora de comenzar/terminar X!"

#### `check_task_deadlines()` (cada 1 minuto)
- Revisa todas las tareas no personales
- Si una tarea vence hoy (deadline en los últimos 2 minutos)
- Y no se notificó al creador
- → Crea una notificación: "Vence hoy: tarea X de estudiante Y"

**Importancia:** Sin esto, los usuarios tendrían que estar mirando el reloj constantemente. El scheduler lo hace por ellos.

---

### `apps/schedule/forms.py`

**¿Qué es?** Formulario para crear/editar entradas de horario.

**Qué valida:**
- La hora de fin debe ser posterior a la hora de inicio
- No puede superponerse con otra entrada existente (mismo día y horario que se pise)
- Para PROGRAMMER, los tipos de entrada se limitan a: Materia, Descanso, Comida

**Importancia:** Evita horarios imposibles (fin antes de inicio) y superposiciones (dos clases al mismo tiempo).

---

### `apps/schedule/utils.py`

**¿Qué es?** Utilidad para construir la **grilla** del horario.

**Qué hace `build_schedule_table()`:**
1. Toma todas las entradas del horario y los días de la semana
2. Extrae todas las horas únicas de las entradas
3. Si no hay entradas, genera slots de 08:00 a 18:00
4. Construye una grilla: cada fila es una hora, cada columna es un día
5. Retorna las filas con las entradas correspondientes

**Analogía:** Es como armar una cuadrícula de Excel: filas = horas, columnas = días, celdas = clases.

**Importancia:** Sin esto, el horario se vería como una lista desordenada en vez de una grilla organizada.

---

### `apps/schedule/views/schedule.py`

**¿Qué es?** Las vistas de horarios.

**Qué hace cada vista:**
- `schedule_personal()`: Tu horario personal. Podés agregar, editar y eliminar entradas.
- `schedule_student_course()`: Horario del curso del profesor al que estás vinculado. Solo podés verlo (readonly), no podés editarlo. Solo para STUDENT.
- `schedule_course()`: Horario del curso que administra el profesor. Podés agregar, editar y eliminar entradas. Solo para TEACHER.

**Importancia:** Son las puertas de entrada a los horarios.

---

## Resumen: ¿Cómo se conecta todo?

```
Usuario visita /tasks/
        ↓
config/urls.py dice → apps/tasks/urls.py
        ↓
tasks/urls.py dice → apps/tasks/views/tasks.py → task_list()
        ↓
task_list() llama a → apps/tasks/services.py → get_task_queryset()
        ↓
get_task_queryset() consulta → apps/tasks/models.py → Task
        ↓
Task usa → apps/accounts/cache.py → get_home_stats() (si necesita caché)
        ↓
Resultados se envían a → templates/tasks/task_list.html
        ↓
El usuario ve la página en su navegador
```

**El flujo completo:**
1. **URL** recibe la petición del navegador
2. **View** procesa la petición
3. **Service** ejecuta la lógica de negocio
4. **Model** consulta la base de datos
5. **Cache** acelera las respuestas
6. **Template** renderiza HTML para el navegador
7. **Signal** crea notificaciones automáticas
8. **Form** valida los datos del usuario
9. **Decorator** verifica permisos

---

> **Nota:** Este archivo fue creado para ayudar a principiantes a entender la estructura del proyecto StarStudy 1.0. Cada archivo es una pieza del rompecabezas, y todas trabajan juntas para crear una aplicación de estudio completa y funcional.
