"""Agent orchestrator service (skeleton).

Responsibilities:
- Orchestrate session state and dialog flow
- Use parser to extract filters
- Use query_builder to build parametric SQL
- Use db to execute queries with retries

All functions are placeholders. Implementation will come later.
"""

from typing import Any


async def handle_message(session_id: str | None, message: str) -> dict[str, Any]:
    """Handle an incoming user message and return agent response.

    TODO: implement orchestration logic.
    """
    return {"ok": True, "session_id": session_id, "reply": "placeholder"}
