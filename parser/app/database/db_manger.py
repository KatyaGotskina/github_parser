from datetime import date

from asyncpg.pool import PoolConnectionProxy
from fastapi import Depends

from api.shemas.activity import ActivityModel
from utils.exceptions import CommonDBException
from api.shemas.repository import RepositoryModel
from database.postgres_db import get_db


class DBManager:

    def __init__(self, connection: PoolConnectionProxy) -> None:
        self.connection = connection

    async def get_repositories(self, limit=100) -> list[RepositoryModel]:
        try:
            sequence = await self.connection.fetch("SELECT * FROM top100 LIMIT $1", limit)
        except Exception as err:
            raise CommonDBException(str(err))

        return [
            RepositoryModel(
                repo=row['repo'],
                owner=row['owner'],
                position_cur=row['position_cur'],
                position_prev=row.get('position_prev'),
                stars=row['stars'],
                watchers=row['watchers'],
                open_issues=row['open_issues'],
                forks=row['forks'],
                language=row.get('language')
            ) for row in sequence
        ]

    async def get_repo_id_by_name_and_owner(
            self,
            repo: str,
            owner: str,
    ) -> int | None:
        try:
            sequence = await self.connection.fetch(
                "SELECT id from top100 WHERE repo = $1 and owner = $2",
                f"{owner}/{repo}", owner
            )
        except Exception as err:
            raise CommonDBException(str(err))

        if len(sequence) == 1:
            return sequence[0]['id']
        return None

    async def get_activity(
            self,
            repo_id: int,
            limit: int = 10,
            offset: int = 0,
            since: date = None,
            until: date = None,
    ) -> list[ActivityModel]:
        try:
            query = """
                SELECT * FROM activity 
                WHERE activity.git_id = $1
                AND date >= COALESCE($2, date)
                AND date <= COALESCE($3, date)
                LIMIT $4
                OFFSET $5
            """
            sequence = await self.connection.fetch(query, repo_id, since, until, limit, offset)
        except Exception as err:
            raise CommonDBException(str(err))

        return [
            ActivityModel(
                commits=record['commits'],
                authors=record['authors'],
                date=record['date']
            ) for record in sequence
        ]

    async def get_activity_count(
            self,
            repo_id: int,
    ) -> int:
        try:
            sequence = await self.connection.fetch(
                """
                SELECT COUNT(*) AS count_for_git_id
                FROM activity
                WHERE git_id = $1;
                """,
                repo_id
            )
        except Exception as err:
            raise CommonDBException(str(err))

        return sequence[0]['count_for_git_id']


def get_db_manager(conn: PoolConnectionProxy = Depends(get_db)) -> DBManager:
    return DBManager(conn)
