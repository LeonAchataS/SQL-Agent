"""Security helpers: allowlist checks and sanitization helpers.

This module will contain functions to validate column/table names and ensure
queries only use allowed identifiers.
"""

from typing import Iterable


def is_allowed_column(col: str, allowed: Iterable[str]) -> bool:
    return col in allowed
