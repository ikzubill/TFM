from fastapi import FastAPI
import uvicorn
from routes.api import router as api_router

services_tags = [
    {
        "name": "Busqueda en Udemy",
        "description": "Endpoint que acepta solicitudes que proceden de los alumnos, buscando y recomendando contenido de Udemy",
    },
    {
        "name": "Health Check",
        "description": "Comprobaciones del estado de salud del sistema. Elasticsearch",
    },
]

app = FastAPI(
    title="api-sco",
    version="v1",
    description="version=v1. Api que dispone de servicios de bsqueda y recomendacion de contenidos",
    servers=[{"url": "http://localhost:8000"}],
    openapi_tags=services_tags,
)


def custom_openapi():
    if not app.openapi_schema:
        openapi_schema = app.openapi_original()
        openapi_schema["openapi"] = "3.0.1"
        app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi_original = app.openapi
app.openapi = custom_openapi

app.include_router(api_router)

# Genera la especificación OpenAPI en JSON
openapi_json = app.openapi()

# Guarda el YAML en un archivo directamente
UVICORN_LOGGING_LEVEL = "DEBUG"
if __name__ == "__main__":
    uvicorn.run(
        "main:app", log_level=UVICORN_LOGGING_LEVEL, reload=True
    )  # Levanta en el puerto 8000 por defecto
