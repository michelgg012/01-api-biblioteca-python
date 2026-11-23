"""Modulo para separar los routes del main para mayor proloijidad
- Utilice CamelCase para el nombre de las funciones 
"""

from fastapi import APIRouter, HTTPException, Query
from schemas.books_schemas import book_schema, get_book_filter, patch_book_schema
from services.books_services import book_services
from pathlib import Path

router = APIRouter(prefix="/libros", tags=["Libros"])

project_path = Path(__file__).resolve().parent.parent
service = book_services(project_path / "datos" / "libros.json")


"""Endpoint para agregar libros y guardarlos en un archivo json"""


@router.post("/", status_code=201)
async def addBook(book: book_schema):
    return await service.create_book(book)


"""Endpoint para obtener libros guardados"""


@router.get("/", status_code=200)
async def getBooks(autor: str | None = None,
                   disponible: bool | None = None,
                   desde: int = Query(default=0, ge=0),
                   limite: int = Query(default=100, ge=0),):
    return await service.get_books(
        autor=autor,
        disponible=disponible,
        desde=desde,
        limite=limite,
    )

"""Endpoint: obtener libros por id """


@router.get("/{id}", status_code=200)
async def get_book_by_id(id: int):
    return await service.get_books_by_id(id)


"""Endpoint: eliminar libro por id"""


@router.delete("/{id}", status_code=204)
async def delete_book(id: int):
    await service.delete_book(id)


"""Endpoint: actualizar libro por id"""


@router.put("/{id}", status_code=200)
async def update_book(id: int, book: book_schema):
    return await service.update_books_by_id(id, book)


"""Endpoint: patch actualizar libro pero no todo """


@router.patch('/{id}', status_code=200)
async def patch_book(id: int, book: patch_book_schema):
    return await service.patch_book(id, book)
