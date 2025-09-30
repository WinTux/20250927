# Proyecto IA Asistente

Este proyecto es una aplicación web con Python / Flask para un asistente de IA, usando una base de datos SQLite estática.  
Aquí están las instrucciones para configurar, ejecutar y entender la estructura del proyecto.

---

## Estructura del proyecto
```
20250927/ ← raíz del proyecto
├── herramientas/
│ └── setup_db.py ← script para crear la base de datos SQLite
├── static/ ← archivos estáticos (CSS, JS, imágenes, etc.)
├── templates/ ← plantillas HTML (Jinja2)
├── main.py ← punto de entrada de la aplicación Flask
├── requisitos.txt ← listado de dependencias (requirements)
├── taller.db ← base de datos SQLite generada (archivo de ejemplo)
└── README.md ← este documento
```

Aquí algunas notas sobre carpetas clave:

- **herramientas/**: contiene utilidades del proyecto, como el script para generar la DB.  
- **static/**: contiene recursos estáticos (CSS, JS, imágenes).  
- **templates/**: contiene los archivos de plantilla `.html` que Flask usará con `render_template`.  
- **main.py**: arranca la aplicación Flask.  
- **taller.db**: es el archivo de base de datos SQLite resultante después de ejecutar el script `setup_db.py`.  
- **requisitos.txt**: lista de dependencias del proyecto (versión de cada paquete, etc.).

---

## Instalación y puesta en marcha

Sigue estos pasos para levantar el proyecto en tu máquina local:

### 1. Clonar el repositorio

```bash
git clone https://github.com/WinTux/20250927.git
cd 20250927
```
### 2. Crear un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate     # En Windows: venv\Scripts\activate
```
### 3.Instalar dependencias
```bash
pip install -r requisitos.txt
```

### 4. Generar la base de datos
3 Se ejecuta el siguiente comando:
```bash
python3 herramientas/setup_db.py
```
### 5. Iniciar la aplicación
´´´bash
python3 main.py
´´´
