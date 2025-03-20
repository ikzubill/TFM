from typing import Dict
from pydantic import BaseModel, Field


class CompetencyModel(BaseModel):  # modelo que se espera recibir en la llamada
    """
    Clase para crear un objeto de tipo CompetencyModel, hereda de BaseModel de pydantic

    Args:
        competences (str): Competencias procedentes del alumno y que se deberan satisfacer con determinados cursos que se proporcionaran como resultado
    """

    competences: Dict[str, int] = Field(
        example={
            "Escritura": 5,
            "Lectura": 9,
        }
    )
