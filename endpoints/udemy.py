from fastapi import APIRouter, Body, Request, status, HTTPException
from models.competency_model import CompetencyModel
from typing import Dict, Any
import search_rules.udemy_rules as udemy_rules
from utils.logger import Logger
from endpoints import responses_conf

logger = Logger("/app/log/service_file.log")

router = APIRouter(prefix="/search")

responses = responses_conf.conf_responses()


def validate_udemy_model(udemy_model: CompetencyModel):
    if len(udemy_model.competences) == 0:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El campo 'competences' esta vacio",
        )

    levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for competence_level in udemy_model.competences.items():
        if (
            competence_level[1] not in levels
        ):  # si el nivel no está dentro de los esperados
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"El nivel de la competencia no se puede procesar, tiene que estar entre los siguientes {levels}",
            )


@router.post(
    "/competences",
    description="Busqueda de cursos dada una competencia determinada",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    responses=responses,
)
def search(request: Request, udemy_model: CompetencyModel = Body(...)):
    """
    Recibe un objeto CompetencyModel en el body de la solicitud, para posteriormente buscar informacion en Elasticsearch
    Args:
        request (Request): Recibe el objeto de la solicitud (request) que contiene informacion sobre la solicitud HTTP
        udemy_model (CompetencyModel): Objeto udemy_model con los campos definidos en la clase CompetencyModel
    Returns:
        Dict[str, Any]: Un diccionario con los resultados de la busqueda o un mensaje de error si ocurre una excepcion.
    Raises:
        Exception: Captura cualquier excepcion ocurrida durante la busqueda y devuelve un mensaje de error.
    """

    response_code = 200
    search_url = request.url

    try:
        validate_udemy_model(udemy_model)
        result = udemy_rules.search_udemy_courses(udemy_model)
        if any(
            result["Recomendaciones"].values()
        ):  # si el campo recomendaciones tiene al menos un resultado, se devuelve el resultado, en caso contrario, se lanza una excepción
            log_message = f"POST {search_url}  [status:{response_code}]"
            logger.log_message("info", log_message)
            return result
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="No se encontraron resultados para la busqueda",
        )

    except HTTPException as exception:  # devuelve la excepción generada anteriormente
        logger.log_message(
            "error",
            f"HTTP Exception {request.url} [status:{exception.status_code}]: {exception.detail}",
        )
        raise exception

    except Exception as e:  # si es una excepción no controlada
        logger.log_message("error", f"unexpected error {str(e)}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )
