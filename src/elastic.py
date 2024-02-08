from elasticsearch import Elasticsearch
from src.config import ELASTIC_NODE, ELASTIC_PORT

elastic_client = Elasticsearch(hosts=f'http://{ELASTIC_NODE}:{ELASTIC_PORT}')

