import hashlib
import json
from elasticsearch import Elasticsearch

# Conexión a Elasticsearch
elastic_client = Elasticsearch("http://localhost:9200")


def main():
    """
    Carga los datos de un archivo JSON y los indexa en Elasticsearch.
    """
    try:
        with open("cursos_Business.json", "r", encoding="utf-8") as file:
            data = json.load(file)  # Cargar el JSON correctamente

        # Obtener los cursos de la clave 'results'
        cursos = data.get("results", [])

        # Indexar los cursos
        index_data("tfm", cursos)  # Indexar los cursos
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")


def index_data(index_name, data):
    """
    Indexa una lista de documentos en un índice de Elasticsearch.

    Args:
    - index_name (str): Nombre del índice donde se indexarán los documentos.
    - data (list): Lista de diccionarios que representan los documentos a indexar.

    Returns:
    None
    """
    for doc in data:
        # Extraer los campos relevantes para el índice
        course_data = {
            "id": doc.get("id"),
            "title": doc.get("title"),
            "url": doc.get("url"),
            "price": doc.get("price"),
            "headline": doc.get("headline"),
            "instructors": [
                {
                    "name": instructor.get("display_name"),
                    "job_title": instructor.get("job_title"),
                }
                for instructor in doc.get("visible_instructors", [])
            ],
            "image_url": doc.get("image_480x270"),
            "locale": doc.get("locale", {}).get("title"),
        }

        # Calcular un ID único para el documento
        doc_id = hashlib.sha256(str(doc["id"]).encode("utf-8")).hexdigest()

        try:
            # Intentar recuperar el documento existente
            elastic_client.index(index=index_name, id=doc_id, body=course_data)
            print(f"Indexando documento con ID {doc_id}.")
        except Exception as e:
            print(f"Error al indexar el documento con ID {doc_id}: {e}")


if __name__ == "__main__":
    main()
