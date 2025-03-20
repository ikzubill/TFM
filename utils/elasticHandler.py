import logging
from datetime import datetime
from elastic import elastic_client
import re


def extract_url(log_message):
    """Extrae la URL del mensaje y la parte de interés desde '/search'."""
    url_match = re.search(r"(https?://\S+)", log_message)
    if url_match:
        full_url = url_match.group(0)
        search_match = re.search(r"search\S*", full_url)
        return search_match.group(0) if search_match else full_url
    return None


def extract_status_code(log_message):
    """Extrae el código de estado HTTP del mensaje."""
    status_match = re.search(r"status:(\d{3})", log_message)
    if status_match:
        return int(status_match.group(1))
    status_match = re.search(r"\((\d{3}),", log_message)
    if status_match:
        return int(status_match.group(1))
    return None


def extract_indices(log_message):
    """Extrae los índices del mensaje."""
    index_match = re.search(r"index:\s*(\[[^\]]*\]|[^\s\[]+)", log_message)
    if index_match:
        index_value = index_match.group(0).replace("index:", "").strip(" []")
        return [i.strip().strip("'\"") for i in index_value.split(",")]
    return []


def process_error_message(log_message):
    """Procesa mensajes de error, eliminando metadatos innecesarios."""
    clean_message = re.sub(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - ", "", log_message
    )
    clean_message = clean_message.replace("ERROR - ", "")
    clean_message = re.sub(r"index:\s*\[[^\]]*\]|index:\s*[^\s\[]+", "", clean_message)
    error_message_match = re.search(r"]: (.+)", clean_message)
    return (
        error_message_match.group(1).strip() if error_message_match else clean_message
    )


class ElasticsearchHandler(logging.StreamHandler):
    def __init__(self, index):
        super().__init__()
        self.es = elastic_client  # Usa el cliente de conexión existente
        self.index = index

    def extract_info(self, log_message):
        """Extrae información del mensaje del log."""
        log_url = extract_url(log_message)
        status_code = extract_status_code(log_message)
        indices = extract_indices(log_message)
        clean_message = (
            process_error_message(log_message) if "ERROR" in log_message else None
        )
        return log_url, status_code, clean_message, indices

    def emit(self, record):
        log_entry = self.format(record)

        # Obtener la fecha del log
        log_time = datetime.utcnow()

        # Extraer información del mensaje
        log_url, status_code, clean_message, indices = self.extract_info(log_entry)

        doc = {
            "@timestamp": log_time.isoformat(),
            "year": log_time.year,
            "month": log_time.month,
            "day": log_time.day,
            "level": record.levelname,
            "endpoint_url": log_url,
            "status_code": status_code,
            "clean_message": clean_message,
            "indices": indices,
            "log_entry": log_entry,
        }
        try:
            # Intentar indexar el documento en Elasticsearch
            self.es.index(index=self.index, body=doc)
        except Exception as e:
            # Capturar cualquier error relacionado con la conexión a Elasticsearch.
            error_message = f"Error al intentar enviar log a Elasticsearch: {str(e)}"
            # Puedes registrar el error en el log local o en consola si la conexión falla
            logging.error(error_message)
            # Puedes también agregar un StreamHandler aquí como fallback, si quieres que los logs
            # continúen procesándose en la consola u otro destino cuando hay un error en Elasticsearch
