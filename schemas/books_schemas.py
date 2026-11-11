from pydantic import BaseModel, Field


class book_schema(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    anio: int = Field(ge=1000, le=2100)
    disponible: bool = True


# class get_book_filter(BaseModel):
#     titulo: str = Field(min_length=1),
#     disponible: bool
#     desde: int
#     limite: int
