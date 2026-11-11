""" Para separar la logica de negocio del endpoint """
# Imports
from fastapi import HTTPException
from schemas.books_schemas import book_schema
from pathlib import Path
import json
import os

# Ruta del archivo


def create_path(self):
    # Crear archivo si no existe | w = write
    if not os.path.exists(self.path):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


class book_services:
    def __init__(self, path: Path):
        self.path = path

    async def create_book(self, book: book_schema):

        titulo = book.titulo
        autor = book.autor
        anio = book.anio
        disponible = book.disponible = True

        # Crear archivo si no existe | w = write
        create_path(self)
        # Leer libros existentes | r = read
        with open(self.path, "r", encoding='utf-8') as f:
            try:
                books = json.load(f)
            except json.JSONDecodeError:
                books = []
        if any(
            book["titulo"].lower() == titulo.lower() and
            book["autor"].lower() == autor.lower()
            for book in books
        ):
            raise HTTPException(
                status_code=409,
                detail="El libro ya se encuentra registrado")
        # Generar id unico
        next_id = max((book["id"] for book in books), default=0) + 1

        # Agregar nuevo libro
        book = {
            "id": next_id,
            "titulo": titulo,
            "autor": autor,
            "anio": anio,
            "disponible": disponible
        }
        # Agregar a la lista
        books.append(book)
        # Guardar otra vez el archivo
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)

        return book
