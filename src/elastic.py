from elasticsearch import Elasticsearch
from src.config import ELASTIC_HOST, ELASTIC_PORT


elastic_client = Elasticsearch(f"http://{ELASTIC_HOST}:{ELASTIC_PORT}")

