"""Modulo para separar los routes del main para mayor proloijidad
- Utilice CamelCase para el nombre de las funciones 
"""

from fastapi import APIRouter, HTTPException
from schemas.books_schemas import book_schema, get_book_filter
from services.books_services import book_services
from pathlib import Path

router = APIRouter(prefix="/libros", tags=["Libros"])

project_path = Path(__file__).resolve().parent.parent
service = book_services(project_path / "datos" / "libros.json")


"""Endpoint para agregar libros y guardarlos en un archivo json"""


@router.post("/", status_code=201)
async def addBook(book: book_schema):
    return await service.create_book(book)
