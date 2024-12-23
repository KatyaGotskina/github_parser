import asyncpg
from asyncpg.pool import PoolConnectionProxy

from utils.config import settings


pool = None


async def init_db_pool() -> None:
    global pool
    pool = await asyncpg.create_pool(
        user=settings.DB_USER,
        host=settings.DB_HOST,
        password=settings.DB_PASSWORD
    )


async def get_db() -> PoolConnectionProxy:
    if pool is None:
        raise RuntimeError("Database connection pool is not initialized.")
    async with pool.acquire() as conn:
        yield conn
