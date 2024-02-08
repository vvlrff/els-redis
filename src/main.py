from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.config import REDIS_HOST, REDIS_PORT

from src.celery.router import router as router_tasks
from src.demo_elastic.router import router as router_demo_elastic
from src.elasticsch.router import router as router_elasticsearch
from src.redis.router import router as router_redis

app = FastAPI(
    title="els API"
)

app.include_router(router_tasks)
app.include_router(router_demo_elastic)
app.include_router(router_elasticsearch)
app.include_router(router_redis)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")