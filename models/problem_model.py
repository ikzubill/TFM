from pydantic import BaseModel, Field

class Problem(BaseModel):
    """Clase que define un esquema, utilizado para proporcionar información detallada sobre un error que ocurre en el API

    Args:
        type (str): URL informativa
        title (str): Breve resumen del problema
        status (int): Código de error
        detail (str): Detalles del problema
        instance (str): Endpoint que causo el error
    """
    type: str = Field(example="URL informativa")
    title: str = Field(example="Breve resumen del problema")
    status: int = Field(example=403)
    detail: str = Field(example="Detalles del problema")
    instance: str = Field(example="Endpoint que causó el error")