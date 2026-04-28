import logging
import time
from contextlib import asynccontextmanager
from typing import Callable, Awaitable


from fastapi import FastAPI, Request, Response
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


# from actions.create_superuser import create_superuser
from api import router as api_router
from core.models import db_helper
from core.config import settings


log = logging.getLogger(__name__)

ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
]

CallNext = Callable[[Request], Awaitable[Response]]

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

async def add_process_time_to_requests(
    request: Request,
    call_next: CallNext,
) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.5f}"
    return response

class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, process_time_header_name: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.header_name = process_time_header_name

    async def dispatch(
        self,
        request: Request,
        call_next: CallNext,
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers[self.header_name] = f"{process_time:.5f}"
        return response


@main_app.middleware("http")
async def log_new_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
):
    log.info(
        "Request %s to %s",
        request.method,
        request.url,
    )
    return await call_next(request)

main_app.middleware("http")(add_process_time_to_requests)
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.add_middleware(
    ProcessTimeHeaderMiddleware,
    process_time_header_name="X-Process-Time-New-Again",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, reload=True)
