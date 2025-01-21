from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from metrics import prometheus_metrics, metrics
from utils.exception_handlers import not_found_handler, common_handler, common_db_handler
from api.endpoints.router import base_router
from utils.config import settings
from utils.exceptions import NotFoundException, CommonDBException
from database.postgres_db import init_db_pool, pool
from utils.middleware import CorrelationIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info('START APP')
    # await init_db_pool()

    yield

    # await pool.close()
    logger.info('END APP')


def _add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundException, not_found_handler)
    app.add_exception_handler(CommonDBException, common_db_handler)
    app.add_exception_handler(RuntimeError, common_handler)


def _init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )
    app.middleware('http')(prometheus_metrics)
    app.add_middleware(CorrelationIdMiddleware)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        description="Приложение для работы с данными о репозиториях github",
        version="1.0.0",
        lifespan=lifespan,
    )
    _init_middlewares(app)
    app.include_router(router=base_router)
    app.add_route('/metrics', metrics)
    return app
