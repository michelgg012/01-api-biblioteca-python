from pydantic import BaseModel, Field, model_validator
from fastapi import Query


class book_schema(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    autor: str = Field(min_length=3, max_length=60)
    anio: int = Field(ge=1000, le=2100)
    disponible: bool = True


class get_book_filter(BaseModel):
    autor: str | None = None
    disponible: bool | None = None
    desde: int = Query(default=0, ge=0)
    limite: int = Query(default=100, ge=0)


class patch_book_schema(BaseModel):
    titulo: str | None = Field(default=None, min_length=3, max_length=100)
    autor: str | None = Field(default=None, min_length=3, max_length=60)
    anio: int | None = Field(default=None, ge=1000, le=2100)
    disponible: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_null_values(cls, values):
        if isinstance(values, dict) and any(
            value is None for value in values.values()
        ):
            raise ValueError("Los campos enviados no pueden ser null")

        return values
