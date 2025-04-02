from fastapi import Body
from elasticsearch_dsl import Search, Q
from models.competency_model import CompetencyModel
from elastic import elastic_client


def search_udemy_courses(udemy: CompetencyModel = Body(...)):
    """Realiza una búsqueda en Elasticsearch para encontrar cursos de Udemy en función de las competencias especificadas."""

    results = {"Recomendaciones": {}}  # Mantiene el nombre correcto

    for competence, level in udemy.competences.items():
        index = "tfm"
        search = Search(using=elastic_client, index=index)

        query = Q(
            "bool",
            should=[
                Q("match", title={"query": competence, "boost": 2}),
                Q("match", headline={"query": competence, "boost": 1.5}),
                Q("match", category={"query": competence}),
            ],
            minimum_should_match=1,
        )

        search = search.query(query)

        try:
            response = search[:10].execute()
        except Exception as e:
            return {
                "error": f"Error en la búsqueda: {str(e)}"
            }  # Captura errores de Elasticsearch

        # Verifica que haya resultados antes de intentar acceder
        if not response or len(response) == 0:
            results["Recomendaciones"][competence] = "No se encontraron cursos"
        else:
            results["Recomendaciones"][competence] = [
                {
                    "id": getattr(result, "id", "N/A"),
                    "title": getattr(result, "title", "Sin título"),
                    "headline": getattr(result, "headline", "Sin descripción"),
                    "url": getattr(result, "url", "#"),
                    "price": getattr(result, "price", "Desconocido"),
                    "instructors": list(
                        getattr(result, "instructors", [])
                    ),  # 🔹 Convierte AttrList a lista
                    "_score": getattr(result.meta, "score", 0),
                }
                for result in response
            ]
    return results  # ✅ Solo devuelve un valor
