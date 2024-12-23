from fastapi import Depends, Query
from starlette import status

from api.endpoints.router import base_router
from api.shemas.repository import RepositoryModel
from database.db_manger import DBManager, get_db_manager


@base_router.get(
    "/top100",
    status_code=status.HTTP_200_OK,
    response_model=list[RepositoryModel],
    description="Получение данных о  топ-100 репозиториях"
)
async def get_top100(
        limit: int = Query(
            100,
            ge=1,
            le=100,
            description="Количество записей в ответе. Можно получить меньше 100, но не больше"
        ),
        db: DBManager = Depends(get_db_manager)
):
    return await db.get_repositories(limit=limit)
