from fastapi import FastAPI, HTTPException
import json
import os
from books_schemas import book_schema

app = FastAPI()


@app.get("/", status_code=200)
async def inicio():
    return {"mensaje": "API de la biblioteca"}

"""Endpoint para obtener libros guardados: en proceso"""
# @app.get("/libros")
# async def getBooks():

"""Endpoint para agregar libros y guardarlos en un archivo json"""


@app.post("/libros", status_code=201)
async def addBook(book: book_schema):

    titulo = book.titulo
    autor = book.autor
    anio = book.anio
    disponible = book.disponible = True
    # Ruta del archivo
    path = "datos/libros.json"
    # Crear archivo si no existe | w = write
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    # Leer libros existentes | r = read
    with open(path, "r", encoding='utf-8') as f:
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
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    return book
