from celery import Celery
import time

from src.config import REDIS_HOST, REDIS_PORT

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')

@celery.task
def perform_task():
    # Здесь можно добавить любую фиктивную задачу, например, просто ожидание
    time.sleep(10)  # Задержка в 5 секунд
    return "Фоновая задача выполнена"
