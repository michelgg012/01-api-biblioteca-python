from pydantic import BaseModel, Field
from fastapi import Query


class book_schema(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    anio: int = Field(ge=1000, le=2100)
    disponible: bool = True


class get_book_filter(BaseModel):
    autor: str | None = None
    disponible: bool | None = None
    desde: int = Query(default=0, ge=0)
    limite: int = Query(default=100, ge=0)
