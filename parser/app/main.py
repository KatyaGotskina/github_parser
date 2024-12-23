from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from utils.exception_handlers import not_found_handler, common_handler, common_db_handler
from api.endpoints.router import base_router
from utils.config import settings
from utils.exceptions import NotFoundException, CommonDBException
from database.postgres_db import init_db_pool, pool


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info('START APP')
    await init_db_pool()

    yield

    await pool.close()
    logger.info('END APP')


def _add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundException, not_found_handler)
    app.add_exception_handler(CommonDBException, common_db_handler)
    app.add_exception_handler(RuntimeError, common_handler)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        description="Приложение для работы с данными о репозиториях github",
        version="1.0.0",
        lifespan=lifespan,
    )
    _add_exception_handlers(app)
    app.include_router(router=base_router)

    return app
