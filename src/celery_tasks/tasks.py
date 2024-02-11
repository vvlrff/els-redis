from celery import Celery
import time
import random
from celery.utils.log import get_task_logger
from src.elastic import elastic_client
from src.config import REDIS_HOST, REDIS_PORT
import os

logger = get_task_logger(__name__)
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}")


@celery.task(bind=True)
def perform_task(self, ip: str, login: str, password: str):
    """
    Выполнить программу с заданными параметрами.
    """
    try:
        # Здесь можно добавить логику подключения к удаленному серверу с использованием IP, логина и пароля

        # Имитация выполнения программы с задержкой в 20 секунд
        time.sleep(20)

        # Генерируем случайное число от 1 до 10
        result = random.randint(1, 10)

        # Сохраняем результат в Elasticsearch
        elastic_client.index(index='results', body={
            'result': result,
            'ip': ip,
            'login': login,
            'password': password,
        })

        return {"message": "Программа успешно выполнена", "result": result}
    except Exception as e:
        logger.error("Произошла ошибка при выполнении программы: %s", str(e))

