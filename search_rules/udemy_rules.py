from fastapi import Body
from elasticsearch_dsl import Search, Q
from models.competency_model import CompetencyModel
from elastic import elastic_client


def search_udemy(udemy: CompetencyModel = Body(...)):
    """Se encarga de realizar la busqueda en Elasticsearch, en referencia con la PCO, diferenciando entre un indice u otro segun corresponda
    Args:
        request (Request): Recibe el objeto de la solicitud (request) que contiene informacion sobre la solicitud HTTP
        udemy (CompetencyModel): Objeto udemy con los campos definidos en la clase CompetencyModel
    """
    all_recomendations = {"Recomendaciones": {}}

    for (
        competence,
        nivel,
    ) in (
        udemy.competences.items()
    ):  # búsqueda por cada competencia y devolver recomendaciones

        index = "tfm"

        search = Search(using=elastic_client, index=index)
        q_res = Q(
            "bool",
            must=[
                Q(
                    "nested",
                    path="competencies",
                    query=Q(
                        "bool",
                        must=[
                            Q(
                                "match",
                                **{
                                    "competencies.name": {
                                        "query": competence,
                                        "boost": 2,
                                    }
                                }
                            ),
                            Q("term", **{"competencies.level": nivel}),
                        ],
                    ),
                )
            ],
            should=[
                (
                    Q(
                        "match",
                        subcategory={
                            "query": competence,
                            "boost": 1.5,
                        },
                    )
                ),
                (Q("match", title=competence)),
                (
                    Q(
                        "nested",
                        path="competencies",
                        query=Q(
                            "bool",
                            must=[
                                Q("match", **{"competencies.description": competence})
                            ],
                        ),
                    )
                ),
                (Q("match", description=competence)),
            ],
        )
        search = search.query(q_res)

        response = search[
            :10
        ].execute()  # se limita la respuesta a 3 recomendaciones por competencia
        all_recomendations["Recomendaciones"][competence] = []

        for result in response:  # por cada recomendación de dicha competencia
            result_dict = result.to_dict()
            result_dict["_score"] = result.meta.score
            all_recomendations["Recomendaciones"][competence].append(result_dict)
    return all_recomendations, index
