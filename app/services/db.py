"""Database helpers using asyncpg (skeleton).

This module will create and manage an asyncpg pool and provide safe
parameterized query execution helpers.
"""

from typing import Any
import asyncpg
from app.config import get_settings

_POOL: asyncpg.pool.Pool | None = None


async def init_db_pool() -> None:
    global _POOL
    settings = get_settings()
    dsn = settings.database_url
    if not dsn:
        raise RuntimeError("DATABASE_URL not configured in settings")
    _POOL = await asyncpg.create_pool(dsn)


async def close_db_pool() -> None:
    global _POOL
    if _POOL:
        await _POOL.close()
        _POOL = None


async def fetch(sql: str, *params: Any) -> list[dict]:
    """Execute a SELECT and return rows as list of dicts.

    Uses asyncpg pool and returns list of dictionaries mapping column->value.
    """
    global _POOL
    if _POOL is None:
        await init_db_pool()

    async with _POOL.acquire() as conn:
        stmt = await conn.prepare(sql)
        records = await stmt.fetch(*params)
        results: list[dict] = []
        for r in records:
            results.append(dict(r))
        return results
