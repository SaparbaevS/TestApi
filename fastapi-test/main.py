from contextlib import asynccontextmanager

from fastapi import FastAPI
from actions.create_superuser import create_superuser

from api import router as api_router
from core.models import db_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_superuser()
    # startup
    yield
    # shutdown
    await db_helper.dispose()



main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router)

