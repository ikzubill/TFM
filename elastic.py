from elasticsearch import Elasticsearch
from app_config import environment_config

verify_certs = environment_config["VERIFY_CERTS"]
cert_path_file = environment_config["CERT_PATH_FILE"]

elastic_client = Elasticsearch("http://localhost:9200")
