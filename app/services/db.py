"""Database helpers using asyncpg (skeleton).

This module will create and manage an asyncpg pool and provide safe
parameterized query execution helpers.
"""

from typing import Any


async def init_db_pool(dsn: str) -> None:
    """Initialize DB pool.

    TODO: implement using asyncpg.create_pool
    """
    pass


async def fetch(sql: str, *params: Any) -> list[dict]:
    """Execute a SELECT and return rows as list of dicts.

    TODO: implement actual DB calls.
    """
    return []
