# Descripción Informática - StarStudy 1.0

> Guía completa y profunda de cada archivo del proyecto.
> Explicada para alguien que está empezando a programar.
> Cada archivo tiene 3 secciones: **Funcionamiento**, **Utilidad** e **Importancia**.

---

## Tabla de Contenidos

1. [Conceptos Fundamentales](#conceptos-fundamentales)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Archivos de Configuración (config/)](#archivos-de-configuración)
4. [App: accounts (cuentas de usuario)](#app-accounts)
5. [App: tasks (tareas)](#app-tasks)
6. [App: habits (hábitos)](#app-habits)
7. [App: schedule (horarios)](#app-schedule)
8. [Diagrama de Flujo General](#diagrama-de-flujo-general)

---

## Conceptos Fundamentales

Antes de leer cada archivo, necesitás entender qué es cada concepto:

### ¿Qué es Python?

**Python** es un lenguaje de programación. Piensa en él como un idioma: vos le "hablás" a la computadora en Python y ella te entiende. Python es famoso porque es fácil de leer, como si fuera castellano.

### ¿Qué es Django?

**Django** es un framework web en Python. Un framework es como un kit de construcción de LEGO: viene con piezas prefabricadas (base de datos, login, formularios, seguridad) y vos solo las armás. En vez de construir cada ladrillo desde cero, Django ya lo hizo por vos.

### ¿Qué es una aplicación (app)?

Una **app** es una parte del proyecto con un propósito específico. Nuestro proyecto tiene 4 apps:
- **accounts**: quién es cada usuario
- **tasks**: las tareas que se asignan
- **habits**: los hábitos diarios
- **schedule**: los horarios

Es como un edificio con departamentos: cada departamento hace una cosa diferente, pero todos trabajan juntos.

### ¿Qué es una base de datos?

Una **base de datos** es como una biblioteca gigante donde se guardan todos los datos: usuarios, tareas, notificaciones, etc. Está organizada en **tablas** (como hojas de Excel), cada tabla tiene **columnas** (campos) y **filas** (registros).

### ¿Qué es un model?

Un **model** es la receta para crear una tabla en la base de datos. Define qué datos se guardan y de qué tipo. Por ejemplo, un model de "Usuario" dice: "guardá un email (texto), un rol (opción), y una contraseña (texto)".

### ¿Qué es una view?

Una **view** (vista) es una función que se ejecuta cuando alguien visita una página web. Recibe la petición del usuario, hace algo (consulta la base de datos, procesa datos) y devuelve una respuesta (una página web).

### ¿Qué es una URL?

Una **URL** es la dirección de una página web. Cuando escribís `www.google.com`, esa es la URL. En Django, cada página tiene una URL, y el framework sabe a qué view enviarla.

### ¿Qué es un template?

Un **template** es el diseño visual de la página web. Es un archivo HTML con lugares vacíos que Django llena con datos. Es como un formulario en blanco donde escribís los datos del usuario.

### ¿Qué es un form?

Un **form** (formulario) es un objeto que maneja los datos que el usuario ingresa. Valida que estén bien (email con @, contraseña larga, etc.) y los prepara para guardarlos en la base de datos.

### ¿Qué es un signal?

Un **signal** es una alarma automática. Django puede "escuchar" eventos (como "se creó un usuario nuevo") y ejecutar código automáticamente cuando pasa algo. Es como un timbre que suena solo cuando alguien toca la puerta.

### ¿Qué es un cache?

Un **cache** es un almacenamiento temporal rápido. En vez de buscar la información cada vez que alguien la necesita, la guardás en un lugar rápido y la leés de ahí. Es como anotar algo en un papelito en vez de buscarlo en un libro gigante cada vez.

### ¿Qué es un decorator?

Un **decorador** es una etiqueta que ponés encima de una función para cambiar su comportamiento. Por ejemplo, un decorador puede decir "solo los profesores pueden usar esta función". Es como un candado en una puerta.

### ¿ qué es un signal?

Un **signal** es un evento automático. Cuando pasa algo (como crear un usuario), Django dispara una función que vos definiste. Es como un timbre que suena solo.

### ¿Qué es APScheduler?

**APScheduler** es una librería que ejecuta tareas automáticamente cada cierto tiempo. En nuestro proyecto, revisa hábitos y deadlines cada minuto. Es como un despertador que suena cada 60 segundos y revisa si hay algo que hacer.

### ¿Qué es Fernet (encriptación)?

**Fernet** es un método para encriptar datos. Convierte un texto legible en una cadena de caracteres que nadie puede leer sin la "llave". Es como meter una carta en un sobre cerrado con llave: solo quien tiene la llave puede abrirla.

---

## Estructura del Proyecto

```
StarStudy-1.0/
├── config/                  ← La configuración general del proyecto
│   ├── settings.py          ← Define TODO: base de datos, apps, seguridad, idioma
│   ├── urls.py              ← Mapa de direcciones: cada página a dónde va
│   ├── wsgi.py              ← Punto de entrada para producción (peticiones normales)
│   └── asgi.py              ← Punto de entrada para producción (peticiones en tiempo real)
├── apps/                    ← Las aplicaciones del proyecto
│   ├── accounts/            ← Manejo de usuarios, login, notificaciones
│   │   ├── models.py        ← Tablas de la base de datos (User, Notification)
│   │   ├── cache.py         ← Sistema de caché para respuestas rápidas
│   │   ├── services.py      ← Lógica de negocio (reglas del sistema)
│   │   ├── signals.py       ← Alarmas automáticas (bienvenida al registrarse)
│   │   ├── backends.py      ← Cómo se verifica quién es cada usuario
│   │   ├── decorators.py    ← Quién puede acceder a qué página
│   │   ├── forms.py         ← Formularios de registro y login
│   │   ├── admin.py         ← Panel de administración de Django
│   │   ├── apps.py          ← Configuración de la app
│   │   ├── urls.py          ← Direcciones de las páginas de accounts
│   │   └── views/           ← Las páginas que ve el usuario
│   │       ├── auth.py      ← Registro, login, logout
│   │       ├── home.py      ← Página principal después del login
│   │       └── profile.py   ← Perfil, GitHub, notificaciones
│   ├── tasks/               ← Manejo de tareas asignadas entre usuarios
│   │   ├── models.py        ← Tablas (Task, Comment)
│   │   ├── services.py      ← Lógica de tareas
│   │   ├── signals.py       ← Notificación automática al asignar tareas
│   │   ├── forms.py         ← Formularios de tareas y comentarios
│   │   ├── views/tasks.py   ← CRUD de tareas
│   │   ├── admin.py         ← Panel de administración
│   │   ├── apps.py          ← Configuración de la app
│   │   └── urls.py          ← Direcciones de las páginas de tareas
│   ├── habits/              ← Manejo de hábitos diarios
│   │   ├── models.py        ← Tablas (Habit, HabitCompletion)
│   │   ├── services.py      ← Lógica de hábitos
│   │   ├── views/habits.py  ← CRUD de hábitos (solo STAFF)
│   │   ├── admin.py         ← Panel de administración
│   │   ├── apps.py          ← Configuración de la app
│   │   └── urls.py          ← Direcciones de las páginas de hábitos
│   └── schedule/            ← Manejo de horarios
│       ├── models.py        ← Tabla (ScheduleEntry)
│       ├── services.py      ← Lógica de horarios con caché
│       ├── scheduler.py     ← Tareas automáticas en background (APScheduler)
│       ├── forms.py         ← Formularios de horarios
│       ├── utils.py         ← Construcción de la grilla del horario
│       ├── views/schedule.py← Vistas de horarios
│       ├── admin.py         ← Panel de administración
│       ├── apps.py          ← Configuración de la app (inicia scheduler)
│       └── urls.py          ← Direcciones de las páginas de horarios
├── static/                  ← Archivos estáticos (CSS, imágenes)
├── templates/               ← Plantillas HTML compartidas
├── docs/                    ← Documentación del proyecto
├── manage.py                ← Control remoto del proyecto
├── requirements.txt         ← Lista de librerías necesarias
└── db.sqlite3               ← La base de datos (se crea automáticamente)
```

---

## Archivos de Configuración

---

### `manage.py`

#### Funcionamiento

`manage.py` es un archivo que Django crea automáticamente. Contiene una función `main()` que:

1. **Configura el entorno:** Le dice a Python dónde encontrar la configuración del proyecto (`DJANGO_SETTINGS_MODULE = 'config.settings'`).
2. **Abre el navegador:** Cuando ejecutás `python manage.py runserver`, abre automáticamente el navegador en `http://127.0.0.1:8000` después de 1.5 segundos.
3. **Ejecuta comandos:** Transfiere el control a Django para ejecutar comandos como `runserver`, `migrate`, `createsuperuser`, etc.

**Cómo funciona paso a paso:**
```
Usuario escribe: python manage.py runserver
        ↓
manage.py lee el comando "runserver"
        ↓
Abre el navegador en http://127.0.0.1:8000
        ↓
Django enciende el servidor web
        ↓
El sitio está disponible para usar
```

**Comandos disponibles:**
- `python manage.py runserver` → Enciende el servidor de desarrollo
- `python manage.py migrate` → Crea las tablas de la base de datos
- `python manage.py createsuperuser` → Crea un usuario administrador
- `python manage.py shell` → Abre una consola de Python con el proyecto cargado
- `python manage.py collectstatic` → Recopila archivos estáticos para producción

#### Utilidad

`manage.py` es la herramienta principal para trabajar con el proyecto. Sin él, no podés:
- Encender el servidor
- Modificar la base de datos
- Crear usuarios administradores
- Ejecutar pruebas
- Hacer cualquier cambio estructural

Es como el control remoto de tu tele: sin él, no podés cambiar de canal, subir el volumen, ni hacer nada. Todo se controla desde ahí.

#### Importancia

`manage.py` es el **punto de partida** de todo el proyecto. Es el primer archivo que tocás cuando querés hacer cualquier cosa. Sin él, el proyecto es solo una colección de archivos sin sentido. Es como tener un auto sin llave: todo está ahí, pero no podés moverlo.

Además, es el archivo que los desarrolladores usan constantemente. Cada vez que querés probar algo, encender el servidor, o cambiar la base de datos, usás `manage.py`. Es tan importante que sin él, literalmente no podés hacer nada con el proyecto.

---

### `config/settings.py`

#### Funcionamiento

`settings.py` es el archivo de configuración más grande y importante del proyecto. Contiene **más de 100 configuraciones** que definen cómo funciona todo.

**Secciones principales:**

1. **Variables de entorno (SECRET_KEY, DEBUG, ALLOWED_HOSTS):**
   ```python
   SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-cambiar-en-produccion')
   DEBUG = os.getenv('DEBUG', 'False') == 'True'
   ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
   ```
   - `SECRET_KEY`: Una clave secreta que usa Django para firmar datos (como contraseñas). Si alguien la roba, puede hacer cosas malas.
   - `DEBUG`: Si es `True`, el proyecto muestra errores detallados. Si es `False`, oculta errores (para producción).
   - `ALLOWED_HOSTS`: Qué dominios pueden acceder al sitio. Si está en producción, debe ser el dominio real.

2. **Apps instaladas (INSTALLED_APPS):**
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',      # Panel de administración
       'django.contrib.auth',       # Sistema de usuarios
       'django.contrib.contenttypes', # Tipos de contenido
       'django.contrib.sessions',   # Sesiones de usuario
       'django.contrib.messages',   # Sistema de mensajes
       'django.contrib.staticfiles', # Archivos estáticos (CSS, JS)
       'apps.accounts',             # Nuestra app de cuentas
       'apps.tasks',                # Nuestra app de tareas
       'apps.habits',               # Nuestra app de hábitos
       'apps.schedule',             # Nuestra app de horarios
   ]
   ```
   Aquí le decís a Django qué aplicaciones existen. Es como decirle al edificio cuántos departamentos tiene.

3. **Base de datos:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',  # Tipo de base de datos
           'NAME': BASE_DIR / 'db.sqlite3',          # Dónde está guardada
           'OPTIONS': { 'timeout': 20 },              # Esperar 20 si está ocupada
       }
   }
   ```
   Usa **SQLite** (una base de datos que es un solo archivo). Es como una biblioteca pequeña: no necesita un servidor separado, todo está en un archivo.

4. **Autenticación:**
   ```python
   AUTH_USER_MODEL = 'accounts.User'  # Usa nuestro modelo de usuario personalizado
   AUTHENTICATION_BACKENDS = ['apps.accounts.backends.EmailRoleBackend']  # Login por email + rol
   ```
   Le dice a Django que use NUESTRO usuario (con roles) en vez del usuario básico de Django.

5. **Caché:**
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
           'LOCATION': 'starstudy-cache',
       }
   }
   ```
   Usa **LocMemCache** (caché en memoria del servidor). Es como tener un cuaderno de notas al lado: rápido pero temporal.

6. **Seguridad:**
   ```python
   SECURE_CONTENT_TYPE_NOSNIFF = True  # Evita que el navegador interprete archivos peligrosos
   X_FRAME_OPTIONS = 'DENY'            # Evita que el sitio se abra en un iframe (ataque clickjacking)
   ```
   Estas configuraciones protegen contra ataques comunes.

7. **Archivos estáticos y media:**
   ```python
   STATIC_URL = 'static/'         # URL para archivos estáticos (CSS, JS, imágenes)
   STATICFILES_DIRS = [BASE_DIR / 'static']  # Dónde buscar archivos estáticos
   MEDIA_URL = 'media/'           # URL para archivos subidos por usuarios
   MEDIA_ROOT = BASE_DIR / 'media' # Dónde guardar archivos subidos
   ```

8. **Login:**
   ```python
   LOGIN_URL = 'login'              # A dónde ir si no estás logueado
   LOGIN_REDIRECT_URL = 'home'      # A dónde ir después del login
   LOGOUT_REDIRECT_URL = 'login'    # A dónde ir después del logout
   ```

#### Utilidad

`settings.py` es el archivo que más vas a tocar cuando estés configurando el proyecto. Cada vez que:
- Querés agregar una nueva app
- Querés cambiar la base de datos
- Querés modificar la zona horaria
- Querés activar/desactivar HTTPS
- Querés cambiar el idioma
- Querés configurar el caché

...tocás `settings.py`. Es como el panel de control de una central eléctrica: todo pasa por ahí.

#### Importancia

Si `settings.py` tiene un error, **TODO el proyecto falla**. Es como tener la dirección de tu casa mal escrita: nadie te va a encontrar. Si la `SECRET_KEY` está mal, los usuarios no pueden loguearse. Si la base de datos está mal configurada, no hay datos. Si `DEBUG` está en `True` en producción, los atacantes pueden ver tus errores.

Es el archivo más crítico del proyecto. Un error acá puede romper todo. Por eso tiene tantas configuraciones: cada una controla un aspecto diferente del funcionamiento.

---

### `config/urls.py`

#### Funcionamiento

`config/urls.py` es el **mapa de direcciones** del sitio completo. Cuando alguien visita una URL (como `http://tusitio.com/tasks/`), Django busca en este archivo a qué vista enviarla.

**Cómo funciona paso a paso:**
```
1. Usuario escribe: http://tusitio.com/tasks/
2. Django busca en config/urls.py
3. Encuentra: path('tasks/', include('apps.tasks.urls'))
4. Django dice: "OK, esto es de tasks, voy a apps/tasks/urls.py"
5. En tasks/urls.py busca la URL exacta
6. Encuentra: path('', views.task_list, name='task_list')
7. Django ejecuta la función task_list()
8. La función devuelve una página web
9. El usuario ve la página
```

**Las URLs principales:**
```python
urlpatterns = [
    path('admin/', admin.site.urls),                    # /admin/ → Panel de Django
    path('', include('apps.accounts.urls')),            # / → Páginas de accounts
    path('tasks/', include('apps.tasks.urls')),         # /tasks/ → Páginas de tareas
    path('habitos/', include('apps.habits.urls')),      # /habitos/ → Páginas de hábitos
    path('schedule/', include('apps.schedule.urls')),   # /schedule/ → Páginas de horarios
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Archivos subidos
```

Cada `path()` tiene:
- **Primera parte:** La URL que busca (ej: `tasks/`)
- **Segunda parte:** A dónde enviarla (ej: `apps.tasks.urls`)

La función `static()` agrega soporte para archivos subidos por usuarios (imágenes, PDFs, etc.).

#### Utilidad

Sin `config/urls.py`, Django no sabría a qué página enviar cuando alguien visita una dirección. Es como tener un edificio sin letreros: cada persona entraría a la habitación equivocada.

Este archivo es el **punto central de distribución**. De aquí salen todas las conexiones hacia las apps. Es como una estación de tren: de aquí salen rutas hacia cada destino.

#### Importancia

`config/urls.py` es el **primer filtro** que ve cada petición. Si una URL no está definida acá, Django muestra un error 404 ("Página no encontrada"). Es como un directorio telefónico: si el número no está, no podés llamar.

Además, es el archivo que define la estructura de URLs del sitio. Si querés que tu sitio sea fácil de usar, las URLs deben ser claras y lógicas. Este archivo es el responsable de eso.

---

### `config/wsgi.py` y `config/asgi.py`

#### Funcionamiento

Estos archivos son los **puntos de entrada** para cuando el sitio está en producción (internet real).

**WSGI (Web Server Gateway Interface):**
- Es el estándar para servir páginas web en Python
- Maneja peticiones **normales**: el usuario hace clic, el servidor responde
- Es como la puerta principal de un edificio: por ahí entra todo el mundo

**ASGI (Asynchronous Server Gateway Interface):**
- Es el estándar para peticiones **en tiempo real**
- Maneja cosas como websockets (chat en vivo, notificaciones instantáneas)
- Es como la puerta de emergencia: para cosas que necesitan velocidad

**Cómo funcionan:**
```python
# Ambos hacen lo mismo: configuran el entorno y crean la aplicación
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()  # o get_asgi_application()
```

Básicamente, le dicen al servidor web (como Apache o Nginx): "Acá está la aplicación Django, mandame las peticiones".

#### Utilidad

En desarrollo (cuando estás probando en tu computadora), **no los necesitás**. El comando `python manage.py runserver` usa su propio servidor interno.

Los necesitás solo cuando:
- Subís el sitio a internet real
- Usás un servidor web profesional (Apache, Nginx, Gunicorn)
- Querés soporte para websockets (chat en tiempo real)

#### Importancia

Son archivos **automáticos**: Django los crea y vos rara vez los tocás. Pero son esenciales para la producción. Sin ellos, no podés subir el sitio a internet. Es como la puerta de entrada de un edificio: sin ella, nadie puede entrar, pero vos no la construís, ya viene con el edificio.

---

## App: accounts

> Esta app es la **recepción del edificio**: maneja quién es cada usuario, quién tiene permiso para qué, y las notificaciones.

---

### `apps/accounts/models.py`

#### Funcionamiento

`models.py` define las **tablas de la base de datos**. Cada clase Python se convierte en una tabla real en SQLite.

**Modelo `User` (Usuario):**

Este modelo extiende el usuario básico de Django (`AbstractUser`) y le agrega campos personalizados:

```python
class User(AbstractUser):
    email = models.EmailField()                    # Email (obligatorio)
    role = models.CharField(max_length=20, ...)    # Rol: STUDENT, TEACHER, STAFF, PROGRAMMER
    code = models.CharField(max_length=6, ...)     # Código de 6 caracteres para vincular
    linked_to = models.ForeignKey('self', ...)     # A qué profesor está vinculado
    github_username = models.CharField(...)         # Usuario de GitHub
    github_token = models.TextField(...)           # Token de GitHub encriptado
```

**Cómo funciona cada campo:**

- **email**: El email del usuario. Se usa para loguearse (en vez de un nombre de usuario).
- **role**: El rol del usuario. Hay 4 roles:
  - `STUDENT` → Estudiante (ve tareas asignadas, se vincula a un profesor)
  - `TEACHER` → Profesor (crea tareas, administra el horario del curso)
  - `STAFF` → Personal (ve tareas, administra hábitos)
  - `PROGRAMMER` → Programador (acede a funcionalidades especiales)
- **code**: Un código de 6 caracteres que los profesores generan. Los estudiantes lo usan para vincularse. Es como una contraseña de invitación.
- **linked_to**: Un campo que conecta al estudiante con su profesor. Es una "relación ForeignKey": cada estudiante apunta a un solo profesor.
- **github_username**: El nombre de usuario en GitHub (solo para programadores).
- **github_token**: Un token de GitHub encriptado con Fernet. Es como una contraseña que le da acceso a GitHub.

**Métodos importantes:**

- `set_github_token(raw_token)`: Encripta el token y lo guarda. Convierte el token en una cadena ilegible.
- `get_github_token()`: Desencripta el token y lo retorna. Convierte la cadena ilegible en el token original.
- `save()`: Antes de guardar, genera un código de 6 caracteres si el usuario no tiene uno. Si el código ya existe, genera otro.
- `unread_notifications_count()`: Retorna cuántas notificaciones sin leer tiene el usuario (usa caché).

**Modelo `Notification` (Notificación):**

```python
class Notification(models.Model):
    user = models.ForeignKey(User, ...)     # A quién le llega
    message = models.CharField(max_length=255)  # Qué dice (máximo 255 caracteres)
    link = models.CharField(max_length=255) # A dónde te lleva al hacer clic
    is_read = models.BooleanField(default=False)  # ¿Ya la viste?
    created_at = models.DateTimeField(auto_now_add=True)  # Cuándo llegó
```

**Cómo funciona:**
- Cuando algo importante pasa (asignación de tarea, bienvenida, deadline), se crea una Notification.
- El usuario ve sus notificaciones en la página de notificaciones.
- Cuando hace clic en una notificación, se marca como leída (`is_read = True`).
- El conteo de notificaciones sin leídas se cachea (se guarda temporalmente) para que la página cargue rápido.

#### Utilidad

`models.py` es el **corazón de la base de datos**. Sin estos modelos:
- No podrías guardar usuarios
- No podrías guardar notificaciones
- No podrías saber quién es cada usuario
- No podrías vincular estudiantes a profesores
- No podrías encriptar tokens de GitHub

Es como los planos de un edificio: sin ellos, no sabés qué pisos tiene, cuántos cuartos, ni dónde van las puertas.

#### Importancia

`models.py` es el archivo **más importante de toda la app accounts**. Define la estructura de datos que todo el resto del proyecto usa. Si un campo está mal definido (ej: el email no es obligatorio), todo el sistema se rompe.

Además, define las **relaciones** entre datos: cada notificación pertenece a un usuario, cada usuario puede estar vinculado a un profesor, etc. Estas relaciones son las que hacen que el sistema funcione como un todo coherente.

El uso de `ForeignKey` es crucial: crea conexiones entre tablas que permiten hacer preguntas como "¿cuántas notificaciones tiene Juan?" o "¿qué tareas tiene la clase de María?".

---

### `apps/accounts/cache.py`

#### Funcionamiento

`cache.py` implementa un **sistema de caché** para acelerar las respuestas del servidor. Usa `django.core.cache` con el backend `LocMemCache` (caché en memoria local).

**Cómo funciona el caché:**

Imaginá que tu mamá te pregunta "¿qué hora es?" cada 5 minutos. Tenés dos opciones:
1. **Sin caché:** Mirás el reloj cada vez que pregunta (lento, cansador)
2. **Con caché:** Mirás el reloj una vez, anotás la hora en un papel, y le mostrás el papel cada vez que pregunta (rápido, fácil)

El caché hace exactamente eso: busca la información una vez, la guarda en memoria, y la retorna rápido las veces siguientes.

**Las funciones principales:**

```python
def _get(key, timeout, fetch_fn):
    val = cache.get(key)      # 1. Busca en el caché
    if val is None:            # 2. Si no está...
        val = fetch_fn()       #    ...ejecuta la función para buscarla
        cache.set(key, val, timeout)  # 3. La guarda en el caché
    return val                 # 4. Retorna el valor
```

**Flujo paso a paso:**
```
1. Alguien pregunta: "¿Cuántas notificaciones sin leer tiene Juan?"
2. cache.get('unread_5') → busca en el caché
3. Si está → retorna el número (rápido, 0.001 segundos)
4. Si no está → ejecuta la consulta a la base de datos (lento, 0.5 segundos)
5. Guarda el resultado en el caché con un tiempo de expiración
6. La próxima vez que pregunten lo mismo, lo sabe del caché
```

**Los tiempos de expiración:**
- `unread`: 2 minutos (las notificaciones cambian seguido)
- `home`: 5 minutos (las estadísticas del home no cambian tan rápido)
- `profile`: 5 minutos (las estadísticas del perfil tampoco)
- `schedule`: 30 minutos (el horario cambia muy poco)

**Las funciones de invalidación:**
```python
def invalidate_unread(user):
    _invalidate(f'unread_{user.pk}')
```
Cuando pasa algo que cambia los datos (se creó una notificación, se completó una tarea), se llama a `invalidate_*` para borrar el caché. Así, la próxima vez que alguien pregunte, se busca de nuevo en la base de datos y se guarda el dato nuevo.

#### Utilidad

Sin caché, cada vez que alguien visita una página, el servidor tendría que:
1. Consultar la base de datos (lento)
2. Calcular estadísticas (lento)
3. Contar notificaciones (lento)
4. Devolver la respuesta

Con caché, el servidor:
1. Busca en memoria (ultrarrápido)
2. Si está → lo retorna
3. Si no está → hace lo de arriba y lo guarda

Esto hace que las páginas carguen **mucho más rápido**. En un sitio con muchos usuarios, la diferencia es enorme.

#### Importancia

El caché es **crucial para el rendimiento**. Sin él, cada visita al home haría 6+ consultas a la base de datos. Con él, hace 0 consultas (si el dato está cacheado).

Pero el caché tiene un riesgo: si no lo "invalidás" cuando los datos cambian, el usuario verá datos viejos. Por eso, cada vez que se crea una tarea, se completó una, o se envía una notificación, se llama a `invalidate_*` para borrar el caché viejo.

Es como un cuaderno de notas: si anotás algo y después cambia, tenés que borrar la nota vieja y escribir la nueva. Si no lo hacés, vas a tener información incorrecta.

---

### `apps/accounts/services.py`

#### Funcionamiento

`services.py` contiene la **lógica de negocio** de la app accounts. En programación, "lógica de negocio" significa las reglas de cómo funciona tu aplicación.

**Las funciones principales:**

1. **`get_user_stats(user)`:**
   ```python
   def get_user_stats(user):
       def fetch():
           task_stats = Task.objects.filter(
               Q(assigned_by=user) | Q(assigned_to=user)
           ).aggregate(
               assigned=Count('id', filter=Q(assigned_by=user, is_personal=False)),
               completed=Count('id', filter=Q(assigned_to=user, is_completed=True)),
               pending=Count('id', filter=Q(assigned_to=user, is_completed=False)),
           )
           students = list(user.linked_students.all()) if can_assign else []
           return { 'assigned': ..., 'completed': ..., 'pending': ..., 'students': ... }
       return get_profile_stats(user.pk, fetch)
   ```
   Calcula las estadísticas del perfil: cuántas tareas asignaste, cuántas completaste, cuántas tenés pendientes, y quiénes son tus estudiantes. Usa caché de 5 minutos.

2. **`link_student_to_teacher(user, code)`:**
   ```python
   def link_student_to_teacher(user, code):
       code = code.strip().upper()
       teacher = User.objects.filter(code=code).exclude(role=User.Role.STUDENT).first()
       if teacher:
           user.linked_to = teacher
           user.save(update_fields=['linked_to'])
           return True, teacher
       return False, None
   ```
   Vincula un estudiante a un profesor usando un código. Busca un usuario con ese código que no sea estudiante, y lo conecta.

3. **`connect_github(user, username)` / `disconnect_github(user)`:**
   Conecta o desconecta la cuenta de GitHub de un programador.

4. **`mark_notification_read(notification)`:**
   Marca una notificación como leída y borra el caché de notificaciones no leídas.

#### Utilidad

`services.py` es donde ocurre la **magia**. Las views son solo "puertas de entrada", pero los services son donde se procesan los datos. Si mañana querés cambiar cómo se calculan las estadísticas, solo tocás acá.

Es como la cocina de un restaurante: el mesero (view) toma tu pedido, pero el chef (service) lo prepara. Si querés cambiar la receta, tocás la cocina, no al mesero.

#### Importancia

Separar la lógica en services es una **buena práctica de programación**. Hace el código:
- **Más fácil de entender:** Cada función hace una cosa clara
- **Más fácil de mantener:** Si algo sale mal, sabés dónde buscar
- **Más fácil de probar:** Podés probar cada función por separado
- **Más reutilizable:** Podés usar la misma función en diferentes views

Sin services, la lógica estaría mezclada con las views, haciendo el código confuso y difícil de cambiar.

---

### `apps/accounts/signals.py`

#### Funcionamiento

`signals.py` define **señales automáticas** que se ejecutan cuando pasa algo específico.

**La señal principal:**
```python
@receiver(post_save, sender=User)
def notificar_bienvenida(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            message='¡Bienvenido a StarStudy! Empezá explorando tu perfil.',
            link='/profile/',
        )
        invalidate_unread(instance)
```

**Cómo funciona paso a paso:**
```
1. Un usuario se registra en el sitio
2. Django guarda el usuario en la base de datos
3. Django dispara la señal "post_save" (después de guardar)
4. La función notificar_bienvenida se ejecuta automáticamente
5. Crea una notificación: "¡Bienvenido a StarStudy!"
6. Borra el caché de notificaciones no leídas
7. El usuario ve la notificación en su perfil
```

**Por qué usa `post_save`:** Es una señal que se dispara DESPUÉS de que Django guarda algo en la base de datos. Así sabemos que el usuario ya existe y podemos crearle la notificación.

**El parámetro `created`:** Es un booleano que dice si el usuario es nuevo (`True`) o si se actualizó (`False`). Solo queremos la notificación de bienvenida para usuarios nuevos.

#### Utilidad

Sin signals, tendrías que escribir manualmente "enviar notificación de bienvenida" en cada vista donde se crea un usuario. Si tenés 5 vistas que crean usuarios, tendrías que escribir el mismo código 5 veces.

Con signals, Django lo hace solo. Es como un timbre automático: cuando alguien toca la puerta, el timbre suena sin que vos tengas que estar mirando.

#### Importancia

Los signals hacen el código **más limpio y menos propenso a errores**. Si olvidás escribir "enviar notificación" en una vista, el usuario no recibe la bienvenida. Con signals, eso no puede pasar: la señal se ejecuta SIEMPRE que se crea un usuario.

Además, es un patrón de diseño importante en Django: **separar la lógica automática de la lógica manual**. Las signals son para cosas que pasan "solas", las views son para cosas que el usuario controla.

---

### `apps/accounts/backends.py`

#### Funcionamiento

`backends.py` define un **backend de autenticación personalizado**. Django viene con un backend básico que busca usuarios por nombre de usuario, pero nosotros necesitamos algo diferente: buscar por email Y rol.

**Cómo funciona el login normal de Django:**
```
1. Usuario ingresa: nombre de usuario + contraseña
2. Django busca un usuario con ese nombre
3. Si lo encuentra y la contraseña es correcta → login exitoso
4. Si no → error
```

**Cómo funciona nuestro backend:**
```
1. Usuario ingresa: email + contraseña + rol
2. Django busca un usuario con ese email Y ese rol
3. Si lo encuentra y la contraseña es correcta → login exitoso
4. Si no → error
```

**El código:**
```python
class EmailRoleBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, role=None, **kwargs):
        UserModel = get_user_model()
        if username is None or password is None:
            return None
        try:
            if role:
                user = UserModel.objects.get(email=username, role=role)
            else:
                user = UserModel.objects.filter(email=username).first()
            if user and user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        return None
```

**Por qué es especial:** Permite que el mismo email tenga múltiples cuentas con diferentes roles. Por ejemplo:
- `juan@correo.com` → rol STUDENT (cuenta de estudiante)
- `juan@correo.com` → rol TEACHER (cuenta de profesor)

Esto es útil si una persona tiene diferentes roles en el sistema.

#### Utilidad

Sin este backend, el login no funcionaría como queremos. El usuario tendría que loguearse con nombre de usuario (no email) y no podría tener múltiples roles.

Este backend hace que la experiencia sea más natural: el usuario ingresa su email (que es lo que todos recuerdan) y su rol (para saber a qué cuenta entrar).

#### Importancia

El backend de autenticación es la **primera línea de defensa** contra intrusos. Si está mal implementado, cualquiera podría entrar al sistema. Por eso, verifica tres cosas:
1. ¿El email existe?
2. ¿El rol es correcto?
3. ¿La contraseña coincide?

Si alguna falla, no deja entrar. Es como un guardia de seguridad: verifica credenciales antes de dejar pasar.

---

### `apps/accounts/decorators.py`

#### Funcionamiento

`decorators.py` define **decoradores** que controlan quién puede acceder a qué páginas. Un decorador es una función que modifica el comportamiento de otra función.

**Cómo funciona un decorador:**
```python
@role_required('TEACHER')
def schedule_course(request):
    # Solo profesores pueden ver esto
    ...
```

Es como poner un candado en una puerta. La función `schedule_course` solo se ejecuta si el usuario tiene el rol `TEACHER`. Si no lo tiene, el decorador lo redirige al home con un mensaje de error.

**Los decoradores disponibles:**

1. **`role_required(*roles)`:** El decorador base. Requiere que el usuario tenga uno de los roles especificados.
   ```python
   @role_required('TEACHER', 'STAFF')  # Solo TEACHER o STAFF
   ```

2. **`teacher_required`:** Atajo para `role_required('TEACHER')`.
   ```python
   @teacher_required  # Equivale a @role_required('TEACHER')
   ```

3. **`programmer_required`:** Atajo para `role_required('PROGRAMMER')`.
   ```python
   @programmer_required  # Equivale a @role_required('PROGRAMMER')
   ```

4. **`can_assign_required`:** Solo TEACHER, STAFF o PROGRAMMER (los que pueden asignar tareas).
   ```python
   @can_assign_required  # Equivale a @role_required('TEACHER', 'STAFF', 'PROGRAMMER')
   ```

**Cómo funciona `role_required` paso a paso:**
```
1. Usuario visita /schedule/course/
2. Django ejecuta schedule_course()
3. El decorador @role_required('TEACHER') se ejecuta primero
4. Verifica: ¿el usuario tiene rol TEACHER?
5. Si SÍ → ejecuta schedule_course()
6. Si NO → redirige al home con mensaje: "No tenés permiso"
```

#### Utilidad

Sin decoradores, cualquier usuario podría ver cualquier página. Un estudiante podría ver la página de administración, un profesor podría ver las páginas de programador, etc.

Los decoradores hacen que el sitio sea **seguro y organizado**. Cada página solo es visible para los usuarios que tienen permiso.

#### Importancia

Los decoradores son **esenciales para la seguridad**. Sin ellos, no habría control de acceso. Es como no tener cerraduras en las puertas de tu casa: cualquiera podría entrar a cualquier habitación.

Además, hacen el código **más limpio**. En vez de escribir "if user.role == 'TEACHER'" al principio de cada función, ponés el decorador y listás. Es más legible y menos propenso a errores.

---

### `apps/accounts/forms.py`

#### Funcionamiento

`forms.py` define los **formularios** que el usuario llena para registrarse o loguearse. Cada formulario tiene campos (nombre, email, contraseña) y validaciones (reglas de qué está bien y qué está mal).

**Formulario `RegisterForm` (Registro):**

Campos:
- `email`: Email del usuario (obligatorio)
- `role`: Rol (STUDENT, TEACHER, STAFF, PROGRAMMER)
- `first_name`: Nombre (obligatorio)
- `last_name`: Apellido (obligatorio)
- `password1`: Contraseña (mínimo 8 caracteres)
- `password2`: Repetir contraseña (debe coincidir)
- `code`: Código de vinculación (opcional, solo para estudiantes)

Validaciones:
```python
def clean(self):
    # 1. No podés tener dos cuentas con el mismo email Y rol
    if User.objects.filter(email=email, role=role).exists():
        raise forms.ValidationError('Ya existe un usuario con ese correo y rol.')
    
    # 2. Si ya tenés una cuenta con otro rol, necesitás otro email
    existing_roles = set(User.objects.filter(email=email).values_list('role', flat=True))
    if existing_roles and role not in existing_roles:
        raise forms.ValidationError('Este correo ya está registrado con otro rol.')
    
    # 3. El código de vinculación debe ser válido
    if code and role == User.Role.STUDENT:
        if not User.objects.filter(code=code).exclude(role=User.Role.STUDENT).exists():
            raise forms.ValidationError('El código de invitación no es válido.')
```

**Formulario `CustomLoginForm` (Login):**

Campos:
- `username`: Email (se llama "username" por compatibilidad con Django)
- `password`: Contraseña
- `role`: Rol

Validación:
```python
def clean(self):
    # Verifica que email + rol + contraseña coincidan
    self.user_cache = authenticate(
        request=self.request,
        username=username,
        password=password,
        role=role,
    )
    if self.user_cache is None:
        raise forms.ValidationError('Correo, rol o contraseña incorrectos.')
```

#### Utilidad

Los formularios son la **primera línea de defensa** contra datos incorrectos. Sin ellos, un usuario podría:
- Registrarse con un email sin @
- Poner una contraseña de 1 letra
- Tener dos cuentas con el mismo email y rol
- Usar un código de vinculación inventado

Los formularios validan todo antes de que llegue a la base de datos.

#### Importancia

Los formularios son **críticos para la integridad de los datos**. Si no validás los datos antes de guardarlos, la base de datos se llena de basura. Y una vez que la basura está ahí, es muy difícil de limpiar.

Además, los formularios mejoran la **experiencia del usuario**: si algo está mal, le dicen qué está mal y cómo arreglarlo. En vez de un error genérico, el usuario ve "El email debe tener @" o "Las contraseñas no coinciden".

---

### `apps/accounts/views/home.py`

#### Funcionamiento

`home.py` es la **vista del home** (página principal). Lo primero que ve el usuario después de hacer login.

**Cómo funciona paso a paso:**
```
1. Usuario hace login
2. Django lo redirige al home (/)
3. La función home() se ejecuta
4. Calcula las estadísticas (usa caché de 5 min)
5. Calcula nivel y XP
6. Envía todo al template home.html
7. El usuario ve la página
```

**Las estadísticas que calcula:**
- `pending`: Tareas pendientes (no completadas)
- `overdue`: Tareas vencidas (pasaron de fecha)
- `completed`: Tareas completadas
- `personal`: Tareas personales pendientes
- `recent`: Últimas 5 tareas pendientes
- `recent_pending`: 3 de esas 5 para mostrar

**El sistema de nivel:**
```python
completed_count = stats['completed']  # Cuántas tareas completaste
level = completed_count // 5 + 1      # Cada 5 tareas subís de nivel
xp = completed_count % 5              # Cuántas tareas te faltan para el siguiente nivel
xp_percent = xp * 20                  # Porcentaje de progreso (0%, 20%, 40%, 60%, 80%)
```

**Ejemplo:**
- Completaste 7 tareas → Nivel 2, XP 2 (faltan 3 para nivel 3)
- Completaste 12 tareas → Nivel 3, XP 2 (faltan 3 para nivel 4)

**Optimizaciones:**
- Usa `get_home_stats()` con caché de 5 minutos
- Usa `.only()` para traer solo los campos necesarios
- Usa `select_related()` para evitar consultas N+1
- `recent_pending` se toma de `recent[:3]` (no hace una consulta separada)

#### Utilidad

El home es la **primera impresión** del usuario. Si es lenta o confusa, el usuario no va a querer usar la app. Por eso, está optimizado para cargar rápido y mostrar información clara.

También es el **punto de navegación**: desde ahí, el usuario puede ir a tareas, perfil, notificaciones, etc.

#### Importancia

El home es **la página más visitada** del sitio. Cada vez que el usuario entra, va al home. Si es lenta (porque no tiene caché o hace muchas consultas), el usuario se frustra y se va.

Por eso, tiene 3 optimizaciones clave:
1. **Caché de 5 minutos:** No calcula las estadísticas cada vez
2. **`.only()`:** Trae solo los campos que necesita (no toda la tabla)
3. **`select_related()`:** Evita consultas N+1 (una consulta en vez de 10)

Estas optimizaciones hacen que el home cargue en **milisegundos** en vez de **segundos**.

---

### `apps/accounts/views/profile.py`

#### Funcionamiento

`profile.py` contiene las **vistas del perfil** del usuario.

**Vista `profile()`:**
```
1. Usuario visita /profile/
2. Si es estudiante y envió un código → lo vincula al profesor
3. Calcula las estadísticas del perfil (usa caché)
4. Muestra el perfil con estadísticas
```

**Vista `github_connect()`:**
```
1. Solo programadores pueden usarla
2. Si el usuario envió un username → lo guarda
3. Redirige al perfil
```

**Vista `github_disconnect()`:**
```
1. Borra el username y token de GitHub
2. Redirige al perfil
```

**Vista `notification_list()`:**
```
1. Lista todas las notificaciones del usuario
2. Las pagina (20 por página)
3. Muestra la lista
```

**Vista `notification_read()`:**
```
1. Solo acepta POST (no GET) por seguridad
2. Busca la notificación por PK
3. La marca como leída
4. Redirige al link de la notificación
```

#### Utilidad

El perfil es donde el usuario **gestiona su información**: ve sus estadísticas, se vincula a profesores, conecta GitHub, y ve notificaciones.

Es como la ficha de un socio en un club: tiene todos tus datos y podés hacer cosas desde ahí.

#### Importancia

El perfil es **importante para la experiencia del usuario**. Sin él, no podría:
- Ver cuántas tareas completó
- Vincularse a un profesor
- Conectar GitHub
- Ver notificaciones

Además, la vista `notification_read` es **segura**: solo acepta POST con CSRF, lo que previene ataques CSRF (Cross-Site Request Forgery).

---

### `apps/accounts/views/auth.py`

#### Funcionamiento

`auth.py` contiene las **vistas de autenticación**: registro, login y logout.

**Vista `register()`:**
```
1. Usuario visita /register/
2. Si envió el formulario → valida los datos
3. Si son válidos → crea el usuario
4. Si tiene código de vinculación → lo vincula al profesor
5. Redirige al login
```

**Vista `logout_view()`:**
```
1. Solo acepta usuarios logueados (@login_required)
2. Cierra la sesión
3. Redirige al login
```

**Vista `join(request, code)`:**
```
1. Recibe un código por URL: /join/A1B2C3/
2. Verifica si el código es válido
3. Si es válido → redirige al registro con el código prellenado
4. Si no es válido → muestra error y redirige al registro
```

**El flujo completo de registro:**
```
1. Profesor comparte link: http://tusitio.com/join/A1B2C3/
2. Estudiante hace clic
3. join() verifica el código
4. Redirige a /register/?code=A1B2C3
5. El formulario tiene el código prellenado
6. El estudiante llena sus datos
7. register() crea el usuario y lo vincula al profesor
8. El estudiante puede loguearse
```

#### Utilidad

Estas vistas son **el inicio de todo**. Sin registro, nadie puede crear cuenta. Sin login, nadie puede entrar. Sin logout, nadie puede salir.

Son como la recepción de un club: ahí es donde te inscribís, entrás, o salís.

#### Importancia

Las vistas de autenticación son **críticas para el funcionamiento del sistema**. Sin ellas:
- Nadie podría crear cuenta
- Nadie podría entrar al sistema
- Nadie podría salir (quedaría logueado para siempre)

Además, `join()` es una funcionalidad **útil para la vinculación**: el profesor comparte un link, el estudiante hace clic, y se vincula automáticamente. Es como una invitación a una fiesta: el anfitrión comparte el link, el invitado entra.

---

## App: tasks

> Esta app es la **sala de tareas**: maneja todo lo relacionado con tareas asignadas entre usuarios.

---

### `apps/tasks/models.py`

#### Funcionamiento

`models.py` define los modelos `Task` (tarea) y `Comment` (comentario).

**Modelo `Task`:**

```python
class Task(models.Model):
    title = models.CharField(max_length=200)           # Título
    description = models.TextField(blank=True)         # Descripción (opcional)
    importance = models.CharField(...)                  # Importancia: LOW, MEDIUM, HIGH, CRITICAL
    deadline = models.DateTimeField(...)                # Fecha límite
    assigned_by = models.ForeignKey(User, ...)          # Quién la creó
    assigned_to = models.ForeignKey(User, ...)          # A quién se la asignaron
    is_completed = models.BooleanField(default=False)   # ¿Está completada?
    completed_at = models.DateTimeField(null=True)      # Cuándo se completó
    is_personal = models.BooleanField(default=False)    # ¿Es personal?
    file = models.FileField(blank=True, null=True)      # Archivo adjunto
```

**Los 4 niveles de importancia:**
- `LOW` → Baja (puede esperar)
- `MEDIUM` → Media (importante)
- `HIGH` → Alta (urgente)
- `CRITICAL` → Crítica (máxima prioridad)

**El orden automático:**
```python
class Meta:
    ordering = [
        Case(
            When(importance='CRITICAL', then=Value(0)),
            When(importance='HIGH', then=Value(1)),
            When(importance='MEDIUM', then=Value(2)),
            When(importance='LOW', then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        ),
        'deadline',
    ]
```
Las tareas se ordenan automáticamente: CRITICAL primero, luego HIGH, MEDIUM, LOW. Dentro de la misma importancia, la que vence primero aparece primero.

**Los 3 índices compuestos:**
```python
indexes = [
    models.Index(fields=['assigned_to', 'is_personal', 'is_completed'], name='idx_task_to_pers_comp'),
    models.Index(fields=['assigned_by', 'is_personal', 'is_completed'], name='idx_task_by_pers_comp'),
    models.Index(fields=['deadline', 'is_completed'], name='idx_task_deadline_comp'),
]
```
Los índices son como el índice de un libro: ayudan a encontrar información más rápido. Sin ellos, la base de datos tendría que buscar en TODAS las filas cada vez.

**Modelo `Comment`:**
```python
class Comment(models.Model):
    task = models.ForeignKey(Task, ...)   # En qué tarea
    user = models.ForeignKey(User, ...)   # Quién lo escribió
    text = models.TextField(...)          # Qué dijo
    created_at = models.DateTimeField(auto_now_add=True)  # Cuándo
```

#### Utilidad

`models.py` define **qué datos se guardan** de las tareas. Sin estos modelos:
- No podrías crear tareas
- No podrías asignar tareas a otros
- No podrías marcar tareas como completadas
- No podrías agregar comentarios
- No podrías filtrar por importancia

Es como los planos de una sala de estudio: define cuántas mesas hay, qué materiales se guardan, y cómo se organizan.

#### Importancia

El modelo Task es **el corazón de la app tasks**. Todo gira alrededor de él: las vistas lo consultan, los services lo modifican, los forms lo validan, y los templates lo muestran.

Los **índices** son especialmente importantes para el rendimiento. Sin ellos, cada consulta a la base de datos sería lenta (porque tendría que buscar en todas las filas). Con ellos, la búsqueda es ultrarrápida.

El **orden automático** es útil para la experiencia del usuario: las tareas más urgentes aparecen primero, sin que el usuario tenga que filtrar.

---

### `apps/tasks/services.py`

#### Funcionamiento

`services.py` contiene la lógica de negocio para las tareas.

**Las funciones principales:**

1. **`get_task_queryset(user, is_personal)`:**
   ```python
   def get_task_queryset(user, is_personal=False):
       if user.role in ('TEACHER', 'STAFF', 'PROGRAMMER'):
           return Task.objects.filter(
               assigned_by=user, is_personal=is_personal,
           ).select_related('assigned_to', 'assigned_by').only(*LIST_FIELDS)
       return Task.objects.filter(
           assigned_to=user, is_personal=is_personal,
       ).select_related('assigned_to', 'assigned_by').only(*LIST_FIELDS)
   ```
   Retorna las tareas según el rol:
   - Profesores/personal/programadores → ven las que CREARON
   - Estudiantes → ven les que les ASIGNARON

2. **`apply_filters(queryset, importance, status, now)`:**
   ```python
   def apply_filters(queryset, importance=None, status=None, now=None):
       if importance:
           queryset = queryset.filter(importance=importance)
       if status == 'pending':
           queryset = queryset.filter(is_completed=False)
       elif status == 'completed':
           queryset = queryset.filter(is_completed=True)
       elif status == 'overdue' and now:
           queryset = queryset.filter(is_completed=False, deadline__lt=now)
       return queryset
   ```
   Filtra tareas por importancia y estado.

3. **`create_task(form, user, is_personal)`:**
   ```python
   def create_task(form, user, is_personal=False):
       task = form.save(commit=False)
       task.assigned_by = user
       if is_personal:
           task.is_personal = True
           task.assigned_to = user
       task.save()
       _invalidate_task_caches(user)
       if task.assigned_to != user:
           _invalidate_task_caches(task.assigned_to)
       return task
   ```
   Crea una tarea y invalida caches.

4. **`complete_task(task, user)`:**
   Marca como completada, envía notificación, invalida caches.

5. **`delete_task(task)`:**
   Captura datos antes de borrar, elimina, invalida caches.

6. **`add_comment(task, user, text)`:**
   Crea un comentario en la tarea.

#### Utilidad

`services.py` es donde se **procesan las tareas**. Las views solo toman decisiones de navegación, pero los services hacen el trabajo pesado.

Si mañana querés cambiar cómo se crean las tareas, solo tocás acá. No tenés que buscar entre 10 views.

#### Importancia

Separar la lógica en services hace el código:
- **Más mantenible:** Si algo sale mal, sabés dónde buscar
- **Más reutilizable:** Podés usar las mismas functions en diferentes views
- **Más testeable:** Podés probar cada función por separado
- **Más legible:** Cada función hace una cosa clara

Sin services, la lógica estaría mezclada con las views, haciendo el código confuso y difícil de mantener.

---

### `apps/tasks/signals.py`

#### Funcionamiento

`signals.py` define una señal que se ejecuta cuando se crea una tarea.

**La señal:**
```python
@receiver(post_save, sender=Task)
def notificar_tarea_asignada(sender, instance, created, **kwargs):
    if created and not instance.is_personal and instance.assigned_to != instance.assigned_by:
        Notification.objects.create(
            user=instance.assigned_to,
            message=f'{instance.assigned_by.get_full_name() or instance.assigned_by.email} te asignó: {instance.title}',
            link=f'/tasks/{instance.pk}/',
        )
        invalidate_unread(instance.assigned_to)
```

**Cómo funciona paso a paso:**
```
1. Profesor crea una tarea para un estudiante
2. Django guarda la tarea en la base de datos
3. La señal post_save se dispara
4. Verifica: ¿Es nueva? ¿No es personal? ¿El creador es diferente al destinatario?
5. Si todo es SÍ → crea una notificación para el estudiante
6. Borra el caché de notificaciones no leídas
7. El estudiante ve la notificación: "Juan te asignó: tarea X"
```

**Las 3 condiciones:**
1. `created`: Solo para tareas nuevas (no para actualizaciones)
2. `not instance.is_personal`: Las tareas personales no generan notificación
3. `assigned_to != assigned_by`: Si te asignás una tarea a vos mismo, no necesitás notificación

#### Utilidad

Sin esta señal, el estudiante no sabría que le asignaron una tarea hasta que entre manualmente a mirar la lista. Con la señal, recibe una notificación automática.

Es como un timbre que suena cuando te llega un paquete: sin él, tendrías que estar revisando la puerta constantemente.

#### Importancia

La señal es **importante para la comunicación**. Hace que el sistema sea proactivo: en vez de esperar a que el usuario mire, le avisa automáticamente.

Además, es un buen ejemplo de por qué los signals son útiles: la lógica de "notificar al asignado" no depende de ninguna view en particular. Puede pasar desde cualquier vista que cree tareas. Con signals, la lógica está centralizada y se ejecuta siempre.

---

### `apps/tasks/forms.py`

#### Funcionamiento

`forms.py` define los formularios para crear tareas y comentarios.

**Formulario `TaskForm`:**

Campos:
- `title`: Título de la tarea
- `description`: Descripción detallada
- `importance`: Importancia (LOW, MEDIUM, HIGH, CRITICAL)
- `deadline`: Fecha límite (formato datetime-local)
- `assigned_to`: A quién se la asignás
- `file`: Archivo adjunto (opcional)

**Lógica especial:**
```python
def __init__(self, *args, **kwargs):
    user = kwargs.pop('user', None)
    super().__init__(*args, **kwargs)
    if user and user.role != User.Role.STUDENT:
        self.fields['assigned_to'].queryset = User.objects.filter(role=User.Role.STUDENT)
    elif user:
        self.fields.pop('assigned_to', None)
```
- Si el usuario es profesor/personal/programador → el campo "asignado a" muestra solo estudiantes
- Si el usuario es estudiante → el campo "asignado a" desaparece (se asigna a sí mismo)

**Formulario `CommentForm`:**

Un solo campo: texto del comentario.

#### Utilidad

Los formularios **validan los datos** antes de que lleguen a la base de datos. Sin ellos:
- Podrías crear una tarea sin título
- Podrías poner una fecha límite en el pasado
- Podrías asignarle una tarea a un profesor (en vez de a un estudiante)

Los formularios evitan estos errores.

#### Importancia

Los formularios son **la puerta de entrada** a la base de datos. Si no validás los datos, la base de datos se llena de basura. Y una vez que la basura está ahí, es muy difícil de limpiar.

Además, la lógica de "mostrar solo estudiantes" es importante para la **experiencia del usuario**: el profesor no ve la lista de todos los usuarios, solo los estudiantes a los que puede asignar tareas.

---

### `apps/tasks/views/tasks.py`

#### Funcionamiento

`tasks.py` contiene las **vistas de las tareas**: las páginas que ve el usuario.

**Vista `task_list()`:**
```
1. Usuario visita /tasks/
2. Obtiene las tareas según su rol
3. Aplica filtros (importancia, estado)
4. Pagina (10 por página)
5. Muestra la lista
```

**Vista `task_personal()`:**
```
1. Atajo a task_list() con is_personal=True
2. Muestra solo las tareas personales
```

**Vista `task_detail()`:**
```
1. Usuario hace clic en una tarea
2. Obtiene la tarea por PK
3. Verifica que el usuario tenga permiso (creador o destinatario)
4. Obtiene los comentarios (paginados)
5. Muestra el detalle
```

**Vista `task_create()`:**
```
1. Solo TEACHER, STAFF, PROGRAMMER pueden crear tareas
2. Muestra el formulario
3. Si es válido → crea la tarea
4. Redirige al detalle
```

**Vista `task_complete()`:**
```
1. Solo acepta POST
2. Verifica que el usuario tenga permiso
3. Marca la tarea como completada
4. Redirige a la lista
```

**Vista `task_delete()`:**
```
1. Solo acepta POST
2. Verifica que el usuario sea el creador
3. Elimina la tarea
4. Redirige a la lista
```

**Vista `comment_create()`:**
```
1. Solo acepta POST
2. Verifica permisos
3. Crea el comentario
4. Redirige al detalle
```

#### Utilidad

Estas vistas son **las puertas de entrada** a las tareas. Cada URL lleva a una vista diferente:
- `/tasks/` → task_list
- `/tasks/personal/` → task_personal
- `/tasks/create/` → task_create
- `/tasks/1/` → task_detail
- `/tasks/1/complete/` → task_complete
- `/tasks/1/delete/` → task_delete
- `/tasks/1/comment/` → comment_create

#### Importancia

Las vistas son **lo que ve el usuario**. Si son confusas o lentas, el usuario no va a querer usar la app.

Por eso, están optimizadas:
- `task_list` usa caché y `.only()` para cargar rápido
- `task_detail` usa `select_related()` para evitar consultas N+1
- `task_complete` y `task_delete` solo aceptan POST (por seguridad)

---

## App: habits

> Esta app es el **cuaderno de hábitos**: maneja los hábitos diarios de los usuarios (solo STAFF).

---

### `apps/habits/models.py`

#### Funcionamiento

`models.py` define los modelos `Habit` (hábito) y `HabitCompletion` (registro de completación).

**Modelo `Habit`:**
```python
class Habit(models.Model):
    user = models.ForeignKey(User, ...)       # De quién es
    title = models.CharField(max_length=200)  # Nombre del hábito
    start_time = models.TimeField(default='00:00')  # Hora de inicio
    end_time = models.TimeField(default='00:00')    # Hora de fin
    level = models.PositiveIntegerField(default=1)   # Nivel actual
```

**Cómo funciona:**
- Cada hábito tiene un título (ej: "Leer 30 minutos")
- Tiene una hora de inicio y fin (para las notificaciones del scheduler)
- Tiene un nivel que sube cada vez que se completa

**Modelo `HabitCompletion`:**
```python
class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, ...)  # De qué hábito es
    date = models.DateField(auto_now_add=True)  # Qué día se completó
```

**La regla `unique_together`:**
```python
class Meta:
    unique_together = ['habit', 'date']
```
Un hábito solo se puede completar UNA vez por día. Si intentás completarlo dos veces el mismo día, la base de datos lo rechaza.

**Método `completed_today()`:**
```python
def completed_today(self):
    return self.completions.filter(date=timezone.localdate()).exists()
```
Verifica si el hábito ya se completó hoy. Usa `timezone.localdate()` en vez de `date.today()` para respetar la zona horaria.

#### Utilidad

Estos modelos permiten **trackear hábitos diarios**. Sin ellos:
- No podrías crear hábitos
- No podrías marcar si los completaste hoy
- No podrías ver cuántas veces completaste un hábito
- No podrías subir de nivel

Es como un cuaderno de hábitos pero digital y automático.

#### Importancia

Los modelos de hábitos son **el corazón de la app habits**. Definen la estructura de datos que todo el sistema usa.

El `unique_together` es especialmente importante: evita que un hábito se cuente dos veces el mismo día. Sin eso, el sistema de niveles no funcionaría correctamente.

El uso de `timezone.localdate()` en vez de `date.today()` es una **buena práctica**: respeta la zona horaria del usuario, no la del servidor.

---

### `apps/habits/services.py`

#### Funcionamiento

`services.py` contiene la lógica de negocio para hábitos.

**Función `toggle_habit(habit)`:**
```python
def toggle_habit(habit):
    today = timezone.now().date()
    _, created = HabitCompletion.objects.get_or_create(
        habit=habit,
        date=today,
    )
    if not created:
        return False, habit  # Ya estaba completado hoy
    habit.level += 1
    habit.save(update_fields=['level'])
    return True, habit  # Se completó, subió de nivel
```

**Cómo funciona paso a paso:**
```
1. Usuario hace clic en "Completar" para un hábito
2. toggle_habit() busca si ya existe una completación hoy
3. Si NO existe → la crea (get_or_create)
4. Si ya existía → no hace nada (no se puede completar dos veces)
5. Si se creó → sube el nivel del hábito (+1)
6. Retorna (created, habit)
```

**El método `get_or_create`:**
Es un método de Django que hace dos cosas en uno:
- Busca si existe un registro con esos datos
- Si no existe, lo crea
- Retorna (objeto, created): created es True si lo creó, False si ya existía

Es como decir: "Mirá si ya tengo esto. Si no lo tengo, crealo."

**Función `create_habit(user, title, start_time, end_time)`:**
Crea un hábito nuevo con los datos del formulario.

**Función `delete_habit(habit)`:**
Elimina un hábito y retorna su título para mostrar un mensaje de éxito.

#### Utilidad

`services.py` es donde ocurre la **magia de los hábitos**: toggle, crear, eliminar.

La función `toggle_habit` es especialmente importante: implementa la lógica de "completar una vez por día" y "subir nivel al completar".

#### Importancia

Sin `services.py`, la lógica de hábitos estaría mezclada con las views, haciendo el código confuso y difícil de mantener.

La función `toggle_habit` es el **corazón del sistema de niveles**: cada vez que completás un hábito, tu nivel sube. Sin ella, no habría gamificación (el sistema de niveles y XP).

---

### `apps/habits/views/habits.py`

#### Funcionamiento

`habits.py` contiene las vistas de hábitos (solo STAFF puede usarlas).

**Vista `habito_list()`:**
```python
@role_required('STAFF')
def habito_list(request):
    today = timezone.localdate()
    habits = request.user.habits.all().annotate(
        total_completions=Count('completions'),
        completed_today=Exists(
            HabitCompletion.objects.filter(
                habit_id=OuterRef('pk'),
                date=today,
            )
        ),
    )
    return render(request, 'habits/habito_list.html', {'habits': habits})
```

**Optimización N+1:**
En vez de hacer una consulta para obtener los hábitos y otra para cada hábito (N+1), hace UNA sola consulta con anotaciones:
- `total_completions`: Cuántas veces se completó en total
- `completed_today`: ¿Ya se completó hoy?

Esto reduce las consultas de **11 a 1** (1 para los hábitos + 10 para cada hábito → 1 con anotaciones).

**Vista `habito_toggle()`:**
```
1. Solo acepta POST
2. Obtiene el hábito por PK
3. Llama a toggle_habit()
4. Si ya estaba completado → muestra error
5. Si se completó → muestra éxito con nivel
6. Redirige a la lista
```

**Vista `habito_create()`:**
```
1. Muestra el formulario
2. Si es válido → crea el hábito
3. Redirige a la lista
```

**Vista `habito_delete()`:**
```
1. Solo acepta POST
2. Obtiene el hábito por PK
3. Lo elimina
4. Redirige a la lista
```

#### Utilidad

Estas vistas son **las puertas de entrada** a los hábitos. El usuario puede:
- Ver sus hábitos (`habito_list`)
- Completar un hábito (`habito_toggle`)
- Crear un hábito nuevo (`habito_create`)
- Eliminar un hábito (`habito_delete`)

#### Importancia

Las vistas de hábitos están **optimizadas para rendimiento**: la consulta N+1 fix reduce las consultas de 11 a 1, haciendo que la página cargue mucho más rápido.

Además, todas las vistas usan `@role_required('STAFF')`: solo el personal puede gestionar hábitos. Los estudiantes y profesores no pueden ver ni modificar hábitos.

---

## App: schedule

> Esta app es el **calendario de horarios**: maneja los horarios personales y de curso.

---

### `apps/schedule/models.py`

#### Funcionamiento

`models.py` define el modelo `ScheduleEntry` (entrada de horario).

**Modelo `ScheduleEntry`:**
```python
class ScheduleEntry(models.Model):
    user = models.ForeignKey(User, ...)       # De quién es
    day = models.CharField(max_length=3)      # Día: MON, TUE, WED, THU, FRI
    start_time = models.TimeField()           # Hora de inicio
    end_time = models.TimeField()             # Hora de fin
    title = models.CharField(max_length=200)  # Nombre (ej: "Matemáticas")
    entry_type = models.CharField(...)        # Tipo: SUBJECT, BREAK, LUNCH
    schedule_type = models.CharField(...)     # Tipo: PERSONAL o COURSE
```

**Los 5 días:**
- `MON` → Lunes
- `TUE` → Martes
- `WED` → Miércoles
- `THU` → Jueves
- `FRI` → Viernes

**Los 3 tipos de entrada:**
- `SUBJECT` → Materia (clase)
- `BREAK` → Recreo
- `LUNCH` → Almuerzo

**Los 2 tipos de horario:**
- `PERSONAL` → Tu horario personal
- `COURSE` → Horario del curso del profesor

**Orden:** Las entradas se ordenan por día y hora de inicio.

#### Utilidad

Este modelo permite **guardar horarios** en la base de datos. Sin él:
- No podrías crear horarios
- No podrías ver el horario del curso
- No podrías diferenciar entre horario personal y de curso

Es como un cuaderno de horarios pero digital y compartido.

#### Importancia

El modelo `ScheduleEntry` es **el corazón de la app schedule**. Define la estructura que todo el sistema usa.

La distinción entre `PERSONAL` y `COURSE` es importante: el horario personal es tuyo, pero el horario del curso lo administra el profesor y los estudiantes solo lo pueden ver.

---

### `apps/schedule/services.py`

#### Funcionamiento

`services.py` contiene la lógica de negocio para horarios.

**Función `get_schedule_context()`:**
```python
def get_schedule_context(user, schedule_type, schedule_name, readonly=False):
    day_values = [d.value for d in ScheduleEntry.Day]
    if readonly and schedule_type == ScheduleEntry.ScheduleType.COURSE:
        teacher = user.linked_to
        if teacher:
            data = get_course_schedule(teacher.pk, lambda: _fetch_schedule(teacher, day_values))
            context = data.copy()
            context.update({ 'schedule_name': schedule_name, 'readonly': readonly })
            return context
    all_entries = list(ScheduleEntry.objects.filter(user=user, schedule_type=schedule_type))
    rows = build_schedule_table(all_entries, day_values)
    return { 'rows': rows, 'days': list(ScheduleEntry.Day), ... }
```

**Cómo funciona:**
1. Si es un estudiante viendo el horario del curso → usa el horario del profesor vinculado con caché de 30 minutos
2. Si es el profesor viendo su horario → carga las entradas directamente
3. Construye la grilla con `build_schedule_table()`

**Función `add_schedule_entry()`:**
Crea una entrada y invalida el caché si es horario de curso.

**Función `delete_schedule_entry()`:**
Elimina una entrada y invalida el caché si es horario de curso.

#### Utilidad

`services.py` maneja la **lógica compleja** de horarios:
- Para estudiantes: carga el horario del profesor (con caché)
- Para profesores: carga su propio horario
- Al crear/eliminar: invalida el caché

Sin estos servicios, la lógica estaría en las views, haciendo el código confuso.

#### Importancia

El caché de 30 minutos para horarios de curso es **importante para el rendimiento**: el horario del curso cambia muy poco (solo cuando el profesor lo modifica), pero muchos estudiantes lo ven. Con caché, el servidor no tiene que cargar el horario cada vez que un estudiante lo mira.

---

### `apps/schedule/scheduler.py`

#### Funcionamiento

`scheduler.py` es el **programador de tareas automáticas**. Usa APScheduler para ejecutar funciones cada cierto tiempo.

**Cómo funciona:**
```python
scheduler = BackgroundScheduler()
_started = False

def start():
    global _started
    if _started:
        return
    scheduler.add_job(check_habit_notifications, 'interval', minutes=1, id='habits')
    scheduler.add_job(check_task_deadlines, 'interval', minutes=1, id='deadlines')
    scheduler.start()
    _started = True
```

**Se ejecuta una vez** cuando el servidor arranca (en `apps/schedule/apps.py` → `ready()`).

**Función `check_habit_notifications()`:**
```
1. Cada 1 minuto, revisa TODOS los hábitos de TODOS los usuarios
2. Para cada hábito, verifica si la hora de inicio o fin está dentro de ±2 minutos
3. Si está dentro de la ventana Y no se notificó hoy → crea notificación
```

**Ejemplo:**
- Hábito: "Leer" de 10:00 a 11:00
- Hora actual: 09:59
- La ventana es: 09:57 a 10:02
- 10:00 está dentro de la ventana → crea notificación: "¡Hora de comenzar Leer!"

**Función `check_task_deadlines()`:**
```
1. Cada 1 minuto, revisa todas las tareas no personales
2. Si una tarea vence hoy (deadline en los últimos 2 minutos)
3. Y no se notificó al creador → crea notificación
```

#### Utilidad

El scheduler es **el despertador del sistema**. Sin él:
- Los usuarios no recibirían notificaciones de hábitos
- Los profesores no sabrían cuándo vencen las tareas
- Todo tendría que ser manual (el usuario tendría que estar revisando)

Con el scheduler, el sistema es **proactivo**: avisa cuando algo importante pasa, sin que el usuario tenga que pedirlo.

#### Importancia

El scheduler es **importante para la experiencia del usuario**. Hace que el sistema sea "inteligente": no solo muestra información, sino que avisa cuando algo necesita atención.

La ventana de ±2 minutos es una **decisión de diseño**: es lo suficientemente amplia para no perder notificaciones (por si el scheduler se retrasa un segundo), pero lo suficientemente estrecha para no enviar notificaciones duplicadas.

---

### `apps/schedule/forms.py`

#### Funcionamiento

`forms.py` define el formulario para crear/editar entradas de horario.

**Formulario `ScheduleEntryForm`:**

Campos:
- `day`: Día de la semana (Lun-Vie)
- `start_time`: Hora de inicio
- `end_time`: Hora de fin
- `title`: Nombre de la materia/actividad
- `entry_type`: Tipo (Materia, Recreo, Almuerzo)

**Validaciones:**
```python
def clean(self):
    # 1. La hora de fin debe ser posterior a la de inicio
    if start_time and end_time and end_time <= start_time:
        raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')
    
    # 2. No puede superponerse con otra entrada
    overlaps = ScheduleEntry.objects.filter(
        user=self._user, day=day,
        start_time__lt=end_time, end_time__gt=start_time,
    )
    if overlaps.exists():
        raise forms.ValidationError('Este horario se superpone con otro existente.')
```

**Para PROGRAMMER:**
```python
if user and user.role == User.Role.PROGRAMMER:
    self.fields['entry_type'].choices = [
        ('SUBJECT', 'Materia'),
        ('BREAK', 'Descanso'),
        ('LUNCH', 'Comida'),
    ]
```

#### Utilidad

El formulario **valida que los horarios sean correctos**. Sin él:
- Podrías poner una hora de fin antes de la de inicio
- Podrías tener dos clases al mismo tiempo
- Podrías crear entradas con datos inválidos

#### Importancia

Las validaciones son **críticas para la integridad de los datos**. Sin ellas, la base de datos se llena de horarios imposibles (ej: clase de 10:00 a 9:00, o dos clases a las 10:00).

---

### `apps/schedule/utils.py`

#### Funcionamiento

`utils.py` contiene la función `build_schedule_table()` que construye la grilla del horario.

**Cómo funciona:**
```python
def build_schedule_table(entries, day_values):
    # 1. Extrae todas las horas únicas de las entradas
    all_times = []
    for e in entries:
        time_str = e.start_time.strftime('%H:%M')
        if time_str not in all_times:
            all_times.append(time_str)
    all_times.sort()
    
    # 2. Si no hay entradas, genera slots de 08:00 a 18:00
    if not all_times:
        all_times = [f'{h:02d}:00' for h in range(8, 18)]
    
    # 3. Construye una grilla: cada fila es una hora, cada columna es un día
    grid = {}
    for e in entries:
        key = (e.day, e.start_time.strftime('%H:%M'))
        if key not in grid:
            grid[key] = []
        grid[key].append(e)
    
    # 4. Retorna las filas
    rows = []
    for slot in all_times:
        cells = []
        for day_value in day_values:
            entries_in_cell = grid.get((day_value, slot), [])
            cells.append(entries_in_cell)
        rows.append((slot, cells))
    
    return rows
```

**Ejemplo:**
Si tenés:
- Lunes 10:00-11:00: Matemáticas
- Martes 10:00-11:00: Historia

La grilla sería:
```
Hora    | Lunes      | Martes     | Miércoles | Jueves | Viernes
10:00   | Matemáticas| Historia   |           |        |
```

#### Utilidad

`build_schedule_table()` convierte una lista de entradas en una **grilla visual** que el template puede mostrar.

Sin esta función, el horario se vería como una lista desordenada:
- Lunes 10:00-11:00 Matemáticas
- Martes 10:00-11:00 Historia
- Lunes 11:00-12:00 Física

Con ella, se ve como una tabla organizada (como un horario de escuela real).

#### Importancia

La grilla es **importante para la experiencia del usuario**. Un horario en formato de tabla es mucho más fácil de leer que una lista de entradas.

Además, la función maneja el caso de "no hay entradas": genera slots de 08:00 a 18:00 para que la grilla no esté vacía.

---

### `apps/schedule/views/schedule.py`

#### Funcionamiento

`schedule.py` contiene las vistas de horarios.

**Vista `schedule_personal()`:**
```
1. Usuario visita /schedule/
2. Si envió un formulario válido → crea entrada
3. Si pidió eliminar → elimina entrada
4. Carga el horario personal
5. Muestra la grilla con formulario
```

**Vista `schedule_student_course()`:**
```
1. Solo para STUDENT
2. Busca el profesor vinculado
3. Si no tiene → muestra error y redirige
4. Carga el horario del profesor (readonly)
5. Muestra la grilla sin formulario
```

**Vista `schedule_course()`:**
```
1. Solo para TEACHER
2. Si envió un formulario válido → crea entrada
3. Si pidió eliminar → elimina entrada
4. Carga el horario del curso
5. Muestra la grilla con formulario
```

#### Utilidad

Estas vistas son **las puertas de entrada** a los horarios:
- `/schedule/` → schedule_personal
- `/schedule/course/` → schedule_course
- `/schedule/student/course/` → schedule_student_course

#### Importancia

Las vistas de horarios están **separadas por rol**:
- Estudiantes solo pueden VER el horario del curso (no editarlo)
- Profesores pueden EDITAR el horario del curso
- Todos pueden gestionar su horario personal

Esta separación es importante para la **seguridad y integridad** de los datos: los estudiantes no pueden modificar el horario del curso.

---

## Diagrama de Flujo General

```
USUARIO
    │
    ▼
NAVEGADOR (escribe URL)
    │
    ▼
config/urls.py (busca a qué app enviar)
    │
    ▼
apps/*/urls.py (busca a qué view enviar)
    │
    ▼
apps/*/views/*.py (procesa la petición)
    │
    ├──→ apps/*/forms.py (valida datos)
    ├──→ apps/*/services.py (ejecuta lógica de negocio)
    │        │
    │        ▼
    │    apps/*/models.py (consulta/modifica la base de datos)
    │        │
    │        ▼
    │    apps/accounts/cache.py (acelera con caché)
    │
    ├──→ apps/accounts/signals.py (crea notificaciones automáticas)
    │
    ▼
templates/*.html (renderiza la página)
    │
    ▼
NAVEGADOR (muestra la página al usuario)
```

**Resumen del flujo:**
1. **URL** recibe la petición del navegador
2. **View** procesa la petición
3. **Form** valida los datos del usuario
4. **Service** ejecuta la lógica de negocio
5. **Model** consulta la base de datos
6. **Cache** acelera las respuestas
7. **Signal** crea notificaciones automáticas
8. **Template** renderiza HTML para el navegador
9. **Decorator** verifica permisos

---

> **Nota:** Este archivo fue creado para ayudar a principiantes a entender la estructura del proyecto StarStudy 1.0. Cada archivo es una pieza del rompecabezas, y todas trabajan juntas para crear una aplicación de estudio completa y funcional.
>
> **Consejo:** Si recién empezás a programar, leé primero los archivos más simples (`manage.py`, `config/settings.py`) y después avanzá hacia los más complejos (`models.py`, `services.py`, `scheduler.py`).
