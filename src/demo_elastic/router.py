from fastapi import APIRouter, HTTPException, status
from src.demo_celery.process_data import process_data, save_processed_data

router = APIRouter(
    prefix="/demo_elasticsearch",
    tags=["Demo_Elasticsearch"]
)

@router.post("/process_and_save_data")
async def process_and_save_data():
    try:
        # Шаг 2: Запуск задачи обработки данных в Celery
        task_result = process_data.delay()

        # Шаг 3: Сохранение задачи в очереди Celery для отслеживания выполнения
        # и начала выполнения другой задачи в случае еще одного вызова данного эндпоинта
        task_id = task_result.id

        # Возвращаем ID задачи для отслеживания статуса выполнения
        return {"task_id": task_id, "status": status.HTTP_200_OK}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check_task_status")
async def check_task_status(task_id: str):
    try:
        # Проверяем статус выполнения задачи в Celery
        task = process_data.AsyncResult(task_id)
        task_status = task.status
        return {"task_id": task_id, "status": task_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
