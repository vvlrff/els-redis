from dotenv import load_dotenv
import os 

load_dotenv()

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
ELASTIC_PORT = os.environ.get('ELASTIC_PORT')