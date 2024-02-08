from fastapi import APIRouter, BackgroundTasks

from src.celery.tasks import perform_task

router = APIRouter()

router = APIRouter(
    prefix="/celery",
    tags=["Celery"]
)

@router.get("/task")
async def perform_background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(perform_task.delay)
    return {"message": "Фоновая задача добавлена в очередь"}
