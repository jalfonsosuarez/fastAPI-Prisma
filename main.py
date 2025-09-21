from fastapi import FastAPI
from user.user import userAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="Mi API de pruebas",
    description="Probando FasAPI",
    summary="Haciendo pruebas con FasAPI y buenas prácticas",
    version="0.0.1",
    contact={
        "name": "José Alfonso Suárez Moreno",
        "email": "joseasuarez@gmail.com",
        "url": "https://jalfonsosuarez.wordpress.com/"
    }
)


@app.get("/", tags=["Root"])
def read_root():
    return {"API running!"}

app.include_router(userAPI)