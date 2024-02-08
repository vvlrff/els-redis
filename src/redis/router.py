from fastapi import APIRouter, HTTPException
from src.redis_cli import get_redis_client

router = APIRouter(
    prefix="/redis",
    tags=["Redis"]
)

@router.post("/", response_model=str)
async def create_item(key: str, value: str):
    """
    Создать новый элемент в Redis.
    """
    try:
        async with get_redis_client() as redis:
            await redis.set(key, value)
        return f"Ключ '{key}' с значением '{value}' успешно создан в Redis"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при создании элемента в Redis: {str(e)}")

@router.get("/{key}", response_model=str)
async def read_item(key: str):
    """
    Получить значение элемента из Redis по ключу.
    """
    try:
        async with get_redis_client() as redis:
            value = await redis.get(key)
            if value is None:
                raise HTTPException(status_code=404, detail=f"Элемент с ключом '{key}' не найден в Redis")
            return value
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при чтении элемента из Redis: {str(e)}")

@router.put("/{key}", response_model=str)
async def update_item(key: str, value: str):
    """
    Обновить значение элемента в Redis по ключу.
    """
    try:
        async with get_redis_client() as redis:
            if not await redis.exists(key):
                raise HTTPException(status_code=404, detail=f"Элемент с ключом '{key}' не найден в Redis")
            await redis.set(key, value)
            return f"Значение элемента с ключом '{key}' успешно обновлено в Redis"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при обновлении элемента в Redis: {str(e)}")

@router.delete("/{key}", response_model=str)
async def delete_item(key: str):
    """
    Удалить элемент из Redis по ключу.
    """
    try:
        async with get_redis_client() as redis:
            if not await redis.exists(key):
                raise HTTPException(status_code=404, detail=f"Элемент с ключом '{key}' не найден в Redis")
            await redis.delete(key)
            return f"Элемент с ключом '{key}' успешно удален из Redis"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при удалении элемента из Redis: {str(e)}")

