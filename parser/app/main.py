from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from core.middleware import DomainErrorMiddleware
from api.endpoints.router import base_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info('START APP')
    yield
    logger.info('END APP')


def _init_middlewares(app: FastAPI) -> None:
    app.add_middleware(DomainErrorMiddleware)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        description="Приложение для работы с данными о репозиториях github",
        version="1.0.0",
        lifespan=lifespan,
    )
    _init_middlewares(app)
    app.include_router(router=base_router)

    return app
