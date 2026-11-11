# Imports
from fastapi import FastAPI
from routes.books import router as book_router

# FastApi
app = FastAPI()
app.include_router(book_router)


@app.get("/", status_code=200)
async def inicio():
    return {"mensaje": "API de la biblioteca"}
