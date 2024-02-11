import aioredis
import logging
from src.config import REDIS_HOST, REDIS_PORT


async def get_redis_pool():
    return await aioredis.create_redis_pool(f'redis://{REDIS_HOST}:{REDIS_PORT}')
