from celery import Celery
from celery.utils.log import get_task_logger
from src.elastic import elastic_client

logger = get_task_logger(__name__)
celery = Celery(__name__)

@celery.task(bind=True)
def process_data(self):
    try:
        # Шаг 1: Получение данных из одного индекса Elasticsearch
        search_results = elastic_client.search(index='source_index', body={"query": {"match_all": {}}})
        hits = search_results['hits']['hits']

        # Шаг 2: Обработка данных (пример)
        processed_data = []
        for hit in hits:
            processed_data.append(hit['_source'])

        # Шаг 3: Сохранение задачи в очереди Celery
        logger.info("Задача успешно обработана, результаты сохранены")
        return "Success"
    except Exception as e:
        logger.error("Произошла ошибка при обработке данных: %s", str(e))
        raise self.retry(exc=e, countdown=10)  # Повторяем задачу через 10 секунд в случае ошибки

@celery.task(bind=True)
def save_processed_data(self, processed_data):
    try:
        # Шаг 4: Сохранение обработанных данных в другой индекс Elasticsearch
        # Пример сохранения данных в новый индекс 'target_index'
        for data in processed_data:
            elastic_client.index(index='target_index', body=data)

        logger.info("Обработанные данные успешно сохранены в индексе 'target_index'")
        return "Success"
    except Exception as e:
        logger.error("Произошла ошибка при сохранении обработанных данных: %s", str(e))
        raise self.retry(exc=e, countdown=10)  # Повторяем задачу через 10 секунд в случае ошибки
