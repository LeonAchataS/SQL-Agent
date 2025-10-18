"""In-memory session manager using ConversationState for storage.

Lightweight wrapper to create, load and persist conversation state and search
results. For MVP it's in-memory; can be swapped for Redis later.
"""

from uuid import uuid4
from typing import Any
from app.models.state import ConversationState


_SESSIONS: dict[str, dict[str, Any]] = {}


def create_session() -> str:
    session_id = str(uuid4())
    _SESSIONS[session_id] = {
        "conversation": ConversationState(session_id=session_id).model_dump(),
        "generated_sql": None,
        "query_results": None,
    }
    return session_id


def get_session(session_id: str) -> dict[str, Any] | None:
    return _SESSIONS.get(session_id)


def save_conversation_state(session_id: str, state: ConversationState) -> None:
    if session_id in _SESSIONS:
        _SESSIONS[session_id]["conversation"] = state.model_dump()


def load_conversation_state(session_id: str) -> ConversationState | None:
    raw = _SESSIONS.get(session_id)
    if not raw:
        return None
    return ConversationState(**raw.get("conversation", {}))


def save_query_result(session_id: str, sql: str, results: list[dict] | None) -> None:
    if session_id in _SESSIONS:
        _SESSIONS[session_id]["generated_sql"] = sql
        _SESSIONS[session_id]["query_results"] = results


def load_query_result(session_id: str) -> tuple[str | None, list[dict] | None]:
    raw = _SESSIONS.get(session_id)
    if not raw:
        return None, None
    return raw.get("generated_sql"), raw.get("query_results")


def reset_session(session_id: str) -> None:
    if session_id in _SESSIONS:
        _SESSIONS[session_id] = {
            "conversation": ConversationState(session_id=session_id).model_dump(),
            "generated_sql": None,
            "query_results": None,
        }


def get_active_sessions_count() -> int:
    return len(_SESSIONS)
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
