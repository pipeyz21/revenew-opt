# Prueba Técnica: Revenew - Backend Django para Optimización de Ingresos

## Acerca de esta Prueba Técnica

En esta prueba técnica desarrollaré una aplicación **backend** con **Django 3.2+** y **Python 3.10**, denominada Revenew, cuyo objetivo es:

* Cargar y validar un archivo CSV con datos de productos (precios, tiempos de máquina, etc.).
* Configurar parámetros de capacidad de producción (tiempo disponible en dos máquinas).
* Ejecutar un **modelo de optimización** (PuLP) que maximiza el ingreso diario sujeto a restricciones de capacidad.
* Presentar los resultados óptimos (cantidades a producir de cada producto y el ingreso total) a través de una interfaz web básica.

Esta prueba técnica está orientada a evaluar habilidades en desarrollo de **backend con Django**, **manipulación de datos** con pandas y la **implementación de modelos matemáticos** de optimización.

---

## Características principales

* **Modularidad**: Separación clara entre la lógica de negocio (DataLoader, OptimizationModel, ResultsHandler) y la capa web (views, templates).
* **Gestión de datos**: Lectura y validación de CSV con pandas.
* **Optimización**: Problema de maximización lineal resuelto con PuLP.
* **UI mínima**: Formulario de subida de CSV, ingreso manual y botón de datos de prueba.
* **Datos de prueba**: botón que carga un CSV de ejemplo desde `data/` y entrega resultados inmediatos.
* **Contenerización**: Dockerfile para reproducir el entorno de Python 3.10 sin conflictos.

---

## Estructura del proyecto

```bash
revenew/                    # Carpeta raíz del repositorio
├── Dockerfile              # Imagen Docker (Python 3.10)
├── requirements.txt        # Dependencias del proyecto
├── .env.sample             # Variables de entorno de ejemplo
├── logs/                   # Archivos de log (app.log)
├── data/                   # CSV de datos de prueba
│   └── optimization_problem_data.csv
├── manage.py               # Punto de entrada de Django
├── revenew/                # Módulo Django del proyecto
│   ├── settings.py         # Configuraciones generales
│   ├── urls.py             # Enrutamiento principal
│   └── wsgi.py             # Interfaz WSGI
└── optimizador/            # App Django principal
    ├── core/               # Lógica del negocio: DataLoader, OptimizationModel, ResultsHandler
    ├── migrations/         # Migraciones
    ├── views.py            # Vistas: index, upload, manual y test
    ├── urls.py             # Rutas de la app
    └── templates/optimizador # Plantillas HTML.
        ├── index.html
        ├── upload.html
        ├── manual.html
        └── resultados.html
```

---

## Requisitos previos

* [Docker](https://www.docker.com/) (recomendado) o:
* Python 3.10
* pip / virtualenv / pyenv / conda

---

## Configuración de variables de entorno

1. Copia `.env.sample` a `.env` en la raíz del proyecto.
2. Edita `.env` con tus valores:
   ```bash
   SECRET_KEY=tu_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
El proyecto carga estas variables al arrancar.

---

## Instalación y ejecución local (sin Docker)

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/pipeyz21/revenew-opt.git
   cd revenew
   ```

2. **Crear y activar entorno virtual**:

   ```bash
   # Con pyenv
   pyenv install 3.10.14
   pyenv virtualenv 3.10.14 revenew-env
   pyenv local revenew-env

   # O con conda
   conda create -n revenew-env python=3.10
   conda activate revenew-env
   ```

3. **Instalar dependencias**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **(Opcional) Migraciones**:

   ```bash
   python manage.py migrate
   ```

5. **Ejecutar servidor de desarrollo**:

   ```bash
   python manage.py runserver
   ```

6. **Abrir en el navegador**:

   > [http://localhost:8000/](http://localhost:8000/)

---

## Ejecución con Docker

1. **Construir la imagen**:

   ```bash
   docker build -t revenew-opt .
   ```

2. **Levantar el contenedor**:

   ```bash
   docker run --rm -p 8000:8000 revenew-opt
   ```

3. **Abrir en el navegador**:

   > [http://localhost:8000/](http://localhost:8000/)

---

## Uso de la interfaz web

- **Landing (`/`)**: elige subir CSV, ingreso manual o datos de prueba.
- **Subir CSV (`/upload/`)**: carga tu CSV y define las capacidades de máquinas.
- **Ingreso Manual (`/manual/`)**: completa manualmente precios, tiempos y capacidades.
- **Resultados**: verás estado, cantidades por producto, ingreso óptimo y gráficos.

---
