from fastapi import status
from models.problem_model import Problem


def conf_responses():
    responses = {
        status.HTTP_200_OK: {
            "description": "Busqueda_exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "type": "https://fastapi.tiangolo.com/tutorial/response-status-code/#changing-the-default",
                        "title": "Búsqueda exitosa",
                        "status": 200,
                        "detail": "Búsqueda exitosa",
                        "instance": "/search/assistant",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No se encontraron resultados para la busqueda",
            "model": Problem,
            "content": {
                "application/json": {
                    "example": {
                        "type": "https://fastapi.tiangolo.com/tutorial/response-status-code/#changing-the-default",
                        "title": "No se encontraron resultados para la busqueda",
                        "status": 404,
                        "detail": "No se han encontrado resultados",
                        "instance": "/search/assistant",
                    }
                }
            },
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Error en la entrada proporcionada",
            "model": Problem,
            "content": {
                "application/json": {
                    "example": {
                        "type": "https://fastapi.tiangolo.com/tutorial/response-status-code/#changing-the-default",
                        "title": "Error en la entrada proporcionada",
                        "status": 422,
                        "detail": "Campo keywords vacio",
                        "instance": "/search/assistant",
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error interno del servidor",
            "model": Problem,
            "content": {
                "application/json": {
                    "example": {
                        "type": "https://fastapi.tiangolo.com/tutorial/response-status-code/#changing-the-default",
                        "title": "Error interno del servidor",
                        "status": 500,
                        "detail": "Error inesperado",
                        "instance": "/search/assistant",
                    }
                }
            },
        },
    }
    return responses
