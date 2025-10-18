"""Query builder (skeleton): build parameterized SELECT queries from filters.

This module must ensure only SELECT queries are produced and use parameter
placeholders compatible with asyncpg ($1, $2...).
"""

from typing import Any, Tuple


def build_property_search_query(filters: dict) -> Tuple[str, Tuple[Any, ...]]:
    """Return (sql, params) for given filters.

    TODO: implement safe builder and allowlist of columns.
    """
    return "SELECT 1", tuple()
