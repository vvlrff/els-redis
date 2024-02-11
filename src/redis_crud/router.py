
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.redis_cli import get_redis_pool
from src.redis_crud.schemas import InputUserMessage
from src.celery_tasks.tasks import perform_task
from celery.result import AsyncResult


router = APIRouter(
    prefix="/redis",
    tags=["Redis"]
)


@router.post("/task", response_model=dict)
async def create_task(search: InputUserMessage):
    """
    Создать задачу и записать ее ID в Redis.
    """
    ip = search.id
    login = search.login
    password = search.password

    try:
        # Запускаем задачу в Celery и получаем ее ID
        task = perform_task.delay(ip, login, password)

        return {"message": "Задача успешно создана", "task_id": task.id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Произошла ошибка при создании задачи: {str(e)}")


@router.get("/tasks")
async def get_all_tasks():
    """
    Получить список всех задач из Redis.
    """
    try:

        redis = await get_redis_pool()
        print("redis", redis)
        celery_keys = await redis.keys("celery-task-meta-*")
        print("keys", celery_keys)
        data = {}
        
        for key in celery_keys:
            print("key", key)
            value = await redis.get(key)
            print("value", value)
            data[key] = value

        return {"data": data}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Произошла ошибка при получении списка задач: {str(e)}")


@router.get("/task/{task_id}", response_model=str)
async def get_task_status(task_id: str):
    """
    Получить состояние задачи по ее ID.
    """
    try:
        # Здесь можно добавить логику проверки, существует ли задача с указанным ID

        # Получаем состояние задачи из Celery
        task_result = AsyncResult(task_id)

        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Произошла ошибка при получении состояния задачи: {str(e)}")
