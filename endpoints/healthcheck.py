from fastapi import APIRouter, HTTPException, status
from elastic import elastic_client


router = APIRouter()


# Función para verificar el estado de salud del clúster de Elasticsearch
def check_elasticsearch_health():
    """comprobar si elasticsearch esta funcionando correctamente

    Raises:
        HTTPException: error 500 si no esta funcionando correctamente

    Returns:
        Dict: informacion de la salud de elasticsearch
    """
    try:
        index_name = "services_logs"
        response = elastic_client.search(
            index=index_name, body={"query": {"match_all": {}}}
        )
        if response["hits"]["total"]["value"] > 0:
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Elasticsearch no devolvió documentos",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al conectar con Elasticsearch: {str(e)}",
        )


# Endpoint para verificar el estado de salud de Elasticsearch
@router.get(
    "/status/elasticsearch",
    description="Verificar el estado de salud del cluster de Elasticsearch",
)
def healthcheck_elasticsearch():
    """se encarga de llamar a la funcion de comprobacion de salud de elasticsearch

    Returns:
        Dict: informacion de salud de elasticsearch
    """
    health_status = check_elasticsearch_health()
    return {"status": health_status}


@router.get(
    "/readiness", description="Comprobar que los servicios estan listos para ser usados"
)
async def readiness():
    return {"status": "ready"}


@router.get(
    "/liveness", description="Comprobar que los servicios estan en funcionamiento"
)
async def liveness():
    return {"status": "alive"}
