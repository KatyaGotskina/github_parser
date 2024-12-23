from datetime import date

from fastapi import Depends, Query, Path
from starlette import status

from api.shemas.activity import ActivityOut, ActivityModel
from utils.exceptions import NotFoundException
from api.endpoints.router import base_router
from database.db_manger import DBManager, get_db_manager


@base_router.get(
    "/{owner}/{repo}/activity",
    status_code=status.HTTP_200_OK,
    response_model=ActivityOut,
    description="Получение данных о коммитах репозитория"
)
async def get_activity(
        owner: str = Path(
            examples=["CryptoSignal"],
            description="Владелец репозитория. owner в таблице top100"
        ),
        repo: str = Path(
            examples=["CryptoSignal"],
            description="""
            Название репозитория. Является одним словом (или набором со спец. символами), но не содержит символ /
            """
        ),
        since: date = Query(None, description="получить коммиты, начиная с указанной даты"),
        until: date = Query(None, description="получить коммиты до указанной даты"),
        limit: int = Query(10, ge=1),
        offset: int = Query(0, ge=0),
        db: DBManager = Depends(get_db_manager)
):
    repo_id = await db.get_repo_id_by_name_and_owner(owner=owner, repo=repo)
    if repo_id is None:
        raise NotFoundException(f"repo with owner = {owner} and name = {repo} not found")

    items: list[ActivityModel] = await db.get_activity(
        repo_id=repo_id,
        since=since,
        until=until,
        limit=limit,
        offset=offset
    )
    count = await db.get_activity_count(repo_id)
    return ActivityOut(items=items, count=count)
