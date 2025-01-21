import random

from fastapi import Depends, Query, Request, Response
from starlette import status

from api.endpoints.router import base_router
from api.shemas.repository import RepositoryModel
from database.db_manger import DBManager, get_db_manager
from utils.logger import logger


@base_router.get(
    "/top100",
    status_code=status.HTTP_200_OK,
    # response_model=list[RepositoryModel],
    description="Получение данных о  топ-100 репозиториях"
)
async def get_top100(
    request: Request,
    limit: int = Query(
        100,
        ge=1,
        le=100,
        description="Количество записей в ответе. Можно получить меньше 100, но не больше"
    ),
    # db: DBManager = Depends(get_db_manager)
):
    logger.info("запрос для получения топ 100 репозиториев", extra={"correlation_id": request.state.correlation_id})
    return random.choice([Response(status_code=200), Response(status_code=400), Response(status_code=500)])
    # return await db.get_repositories(limit=limit)
