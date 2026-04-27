from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# from actions.create_superuser import create_superuser
from api import router as api_router
from core.models import db_helper
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_superuser()
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, reload=True)
