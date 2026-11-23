""" Para separar la logica de negocio del endpoint """
# Imports
from fastapi import HTTPException
from schemas.books_schemas import book_schema, patch_book_schema
from pathlib import Path
import json
import os

# Ruta del archivo


def create_path(self):
    # Crear la carpeta y el archivo si no existen.
    self.path.parent.mkdir(parents=True, exist_ok=True)
    if not self.path.exists():
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def read_json(self):
    with open(self.path, "r", encoding='utf-8') as f:
        try:
            books = json.load(f)
        except json.JSONDecodeError:
            books = []
    return books


# funcion que me ayudo la IA
def get_next_id(self, books):
    count_path = self.path.with_name("next_id.txt")
    minimum_id = max((book["id"] for book in books), default=0) + 1

    if count_path.exists():
        try:
            saved_id = int(count_path.read_text(encoding='utf-8').strip())
            next_id = max(saved_id, minimum_id)
        except ValueError:
            next_id = minimum_id
    else:
        next_id = minimum_id
    count_path.write_text(
        str(next_id + 1),
        encoding='utf-8'
    )
    return next_id


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
        next_id = get_next_id(self, books)
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
        create_path(self)
        books = read_json(self)

        for book in books:
            if book["id"] == id:
                return book

        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    async def update_books_by_id(self, id: int, book: book_schema):
        create_path(self)
        books = read_json(self)

        for index, existing_book in enumerate(books):
            if existing_book["id"] == id:
                updated_book = {
                    "id": id,
                    "titulo": book.titulo,
                    "autor": book.autor,
                    "anio": book.anio,
                    "disponible": book.disponible
                }

                books[index] = updated_book

                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(books, f, ensure_ascii=False, indent=2)

                return updated_book
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado")

    async def patch_book(self, id: int, book: patch_book_schema):
        create_path(self)
        books = read_json(self)

        for existing_book in books:
            if existing_book["id"] == id:
                changes = book.model_dump(exclude_unset=True)

                for field, value in changes.items():
                    existing_book[field] = value

                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(books, f, ensure_ascii=False, indent=2)

                return existing_book

        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    """enderakore  """

    async def delete_book(self, id: int):
        create_path(self)
        books = read_json(self)

        for index, book in enumerate(books):
            if book["id"] == id:
                books.pop(index)

                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(books, f, ensure_ascii=False, indent=2)

                return

        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )
