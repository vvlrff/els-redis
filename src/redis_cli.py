import aioredis
from src.config import REDIS_HOST, REDIS_PORT

async def get_redis_client():
    return await aioredis.create_redis_pool(f'redis://{REDIS_HOST}:{REDIS_PORT}')
