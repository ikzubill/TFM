import logging
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from queue import Queue
from utils.elasticHandler import ElasticsearchHandler
import atexit


class Logger:
    """
    Clase Logger que permite configurar un sistema de logging tanto en consola
    como en archivo. Se puede especificar un archivo de log, si no, solo se logueará
    en consola
    """

    logger_format = "%(asctime)s - %(levelname)s - %(message)s"

    def __init__(self, log_file=None):
        """
        Si se proporciona log_file, agrega un RotatingFileHandler para guardar los logs en ese archivo.
        """
        self.logger_obj = logging.getLogger(__name__)
        self.listener = None
        if not self.logger_obj.hasHandlers():
            self.logger_obj.setLevel(logging.DEBUG)  # Nivel de log predeterminado

            # Crear una cola para manejar los logs asincrónicamente
            log_queue = Queue()

            # Crear manejador de cola
            queue_handler = QueueHandler(log_queue)
            self.logger_obj.addHandler(queue_handler)

            # Crear manejador de consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel("DEBUG")  # Nivel de log para consola
            console_handler.setFormatter(logging.Formatter(self.logger_format))

            handlers = [console_handler]

            if log_file:
                # Crear manejador de archivo con rotación
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=10 * 1024 * 1024,
                    backupCount=5,
                )
                file_handler.setLevel("INFO")  # Nivel de log para archivo
                file_handler.setFormatter(logging.Formatter(self.logger_format))
                handlers.append(file_handler)

            # Crear manejador de Elasticsearch
            es_index = "services_logs"
            if es_index:
                self.es_handler = ElasticsearchHandler(es_index)
                self.es_handler.setLevel("INFO")  # Nivel de log para Elasticsearch
                self.es_handler.setFormatter(logging.Formatter(self.logger_format))
                handlers.append(self.es_handler)

            # Crear un QueueListener para procesar los logs de la cola
            self.listener = QueueListener(log_queue, *handlers)
            self.listener.start()

            # Registrar el método stop_listener para que se llame al salir
            atexit.register(self.stop_listener)

    # Definir mensajes
    def log_message(self, level, message):
        """
        Registra un mensaje con un nivel específico (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        if level.lower() == "debug":
            self.logger_obj.debug(message)
        elif level.lower() == "info":
            self.logger_obj.info(message)
        elif level.lower() == "warning":
            self.logger_obj.warning(message)
        elif level.lower() == "error":
            self.logger_obj.error(message)
        elif level.lower() == "critical":
            self.logger_obj.critical(message)
        else:
            self.logger_obj.info(message)

    def stop_listener(self):
        """
        Detiene el QueueListener.
        """
        if self.listener:
            self.listener.stop()
