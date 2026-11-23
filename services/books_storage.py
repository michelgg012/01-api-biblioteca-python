"""
Funciones relacionadas con la persistencia de libros

El modulo administra la creacion de archivos y carpetas, 
la lectura del json y la generacion del identificador unico.
"""

import json
from pathlib import Path


def create_path(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def read_json(path: Path):
    create_path(path)

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

# funcion para decidir de donde tomar el siguiente id, me ayude con IA para la parte del txt


def get_next_id(path: Path, books: list[dict]):
    counter_path = path.with_name("next_id.txt")
    minimum_id = max((book["id"] for book in books), default=0) + 1

    if counter_path.exists():
        try:
            saved_id = int(counter_path.read_text(encoding="utf-8").strip())
            next_id = max(saved_id, minimum_id)
        except ValueError:
            next_id = minimum_id
    else:
        next_id = minimum_id

    counter_path.write_text(
        str(next_id + 1),
        encoding="utf-8",
    )

    return next_id
