# Proyecto TP — Gestión de Tareas y Horarios

Plataforma educativa con roles (Estudiante, Profesor, Personal, Programador), gamificación y hábitos.

## Requisitos

- Python 3.12+
- pip

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd proyecto-tp

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Abrir http://127.0.0.1:8000/

## Roles

| Rol | Descripción |
|-----|-------------|
| Estudiante | Ve tareas asignadas y horario del curso |
| Profesor | Crea/Asigna tareas, gestiona horarios |
| Personal | Gestiona hábitos con sistema de niveles |
| Programador | Misión interactiva + conexión GitHub |

## Funcionalidades

- Tareas personales y asignadas con niveles de importancia
- Horarios personalizados por rol
- Notificaciones en tiempo real
- Hábitos diarios con subida de nivel
- Código de vinculación estudiante-profesor
- Gamificación (niveles, misiones)
