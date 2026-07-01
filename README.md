# StarStudy 🌟

Plataforma educativa inteligente con roles, gamificación y gestión de hábitos.

Diseñada para conectar **estudiantes**, **profesores**, **personal administrativo** y **programadores** en un solo entorno, con una interfaz temática *Noche Estrellada* al estilo Van Gogh.

---

## ✨ ¿Para qué sirve?

**StarStudy** organiza la vida académica mediante:

| Funcionalidad | Descripción |
|---------------|-------------|
| **Tareas** | Creación, asignación y seguimiento con niveles de importancia (Baja → Crítica). Filtros por estado y urgencia. |
| **Horarios** | Gestión de horarios personales y de curso, con vista tipo mapa interactivo. |
| **Hábitos** | Seguimiento diario con sistema de niveles: cada día que completás un hábito subís de nivel. |
| **Notificaciones** | Alertas al completar tareas, al vencer plazos, y recordatorios de hábitos. |
| **Vinculación** | Profesores generan un código; estudiantes lo usan al registrarse para vincularse automáticamente. |
| **Gamificación** | Sistema de niveles y misiones (visible para rol Programador). |

---

## 👥 Roles

| Rol | Acceso |
|-----|--------|
| **Estudiante** | Tareas asignadas, horario del curso vinculado |
| **Profesor** | Crear/asignar tareas, horarios personales y de clase, código de vinculación |
| **Personal** | Horarios, tareas personales, **sistema de hábitos** "Misión Principal" |
| **Programador** | Vista tipo misión/mapa, conexión con GitHub |

---

## 🖼️ Diseño

- Temática oscura "Noche Estrellada" con acentos dorados (`#ffd54f`)
- Formularios transparentes con borde inferior dorado
- Modal auto-cierre a 3 segundos
- Totalmente responsive

---

## 🛠️ Tecnologías

- **Backend:** Django 6.0
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Base de datos:** SQLite
- **Notificaciones programadas:** APScheduler

---

## ⚙️ Instalación

```bash
# Clonar
git clone https://github.com/tu-usuario/StarStudy.git
cd StarStudy

# Entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/macOS

# Dependencias
pip install -r requirements.txt

# Base de datos
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Abrir http://127.0.0.1:8000/

---

## 🧪 Primeros pasos

1. Registrate con cualquier rol (Estudiante, Profesor, Personal, Programador)
2. Si sos **Profesor**: creá tareas y compartí tu código de vinculación
3. Si sos **Estudiante**: vinculate con el código de un profesor
4. Si sos **Personal**: probá la sección "Misión Principal" (hábitos)
5. Si sos **Programador**: conectá tu cuenta de GitHub

---

## 🤝 Comunidad

**StarStudy** es un proyecto abierto a toda la comunidad educativa y de desarrollo.

- **Usalo** — registrate con tu rol y probá todas las funcionalidades
- **Compartilo** — si te sirve, recomendalo a otros estudiantes o docentes
- **Mejoralo** — si sabés programar, hacé fork, creá una branch y mandá un pull request
- **Reportá bugs** — abrí un issue en GitHub si encontrás algún error
- **Proponé ideas** — cualquier sugerencia es bienvenida

Entre todos podemos hacer de StarStudy una herramienta cada vez mejor para la educación. ¡Sumate y aportá tu granito de estrella! 🌟

---

## 📄 Licencia

Uso educativo.
