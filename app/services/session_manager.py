"""Simple in-memory session manager (skeleton).

This will keep per-session conversation state and collected filters. It's an
in-memory dict for MVP; can be swapped for Redis later.
"""

from typing import Any
from uuid import uuid4

_SESSIONS: dict[str, dict[str, Any]] = {}


def create_session() -> str:
    session_id = str(uuid4())
    _SESSIONS[session_id] = {"messages": [], "filters": {}, "state": {}}
    return session_id


def get_session(session_id: str) -> dict[str, Any] | None:
    return _SESSIONS.get(session_id)


def update_session(session_id: str, data: dict) -> None:
    if session_id in _SESSIONS:
        _SESSIONS[session_id].update(data)
