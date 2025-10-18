"""Agent router (skeleton).

Endpoints here will be the external HTTP surface for interacting with the agent.
Keep actual business logic in services/ to make the router minimal.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import AgentMessage
from app.services import agent_service, session_manager

router = APIRouter()


@router.post("/message")
async def post_message(payload: AgentMessage):
    """Receive a message and forward to the agent service."""
    result = await agent_service.handle_message(payload.session_id, payload.message)
    return result


@router.get("/properties/{session_id}")
async def get_properties(session_id: str):
    """Return last query results for a session (if any)."""
    sql, results = session_manager.load_query_result(session_id)
    if sql is None and results is None:
        raise HTTPException(status_code=400, detail="No search executed for this session")
    return {"session_id": session_id, "count": len(results) if results else 0, "properties": results or [], "sql_query": sql}
