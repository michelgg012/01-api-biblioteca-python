Trabajo integrador:
API REST desarrollada con FastAPI para administrar libros mediante un archivo JSON.

## Requisitos

- Python 3.10 o superior
- FastAPI
- Pydantic
- Uvicorn

## Instalación en Windows

Crear el entorno virtual:

- python -m venv .venv

Instalar dependencias:

- pip install -r requirements.txt

Ejecucion:

- uvicorn main:app --reload

La API estará disponible en:

- http://127.0.0.1:8000

para revisar los endpoints:

- http://127.0.0.1:8000/docs

## Persistencia

Persistencia para los datos de los libros:
datos/libros.json
Persistencia para el id:
datos/next_id.txt
