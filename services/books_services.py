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


def read_json(self):
    with open(self.path, "r", encoding='utf-8') as f:
        try:
            books = json.load(f)
        except json.JSONDecodeError:
            books = []
    return books


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
        books = read_json(self)
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

    async def get_books(self,
                        autor: str | None = None,
                        disponible: bool | None = None,
                        desde: int | None = 0,
                        limite: int = 100):

        # Crear archivo si no existe | w = write
        create_path(self)
        books = read_json(self)

        if autor is not None:
            books = [
                book for book in books
                if book["autor"].lower() == autor.lower()
            ]
        if disponible is not None:
            books = [
                book for book in books
                if book["disponible"] == disponible
            ]
        books = sorted(books, key=lambda book: book["id"])
        return books[desde: desde + limite]

    async def get_books_by_id(self, id: int):
        books = read_json(self)

        for book in books:
            if book["id"] == id:
                return book

        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )
