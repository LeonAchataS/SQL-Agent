"""Agent router (skeleton).

Endpoints here will be the external HTTP surface for interacting with the agent.
Keep actual business logic in services/ to make the router minimal.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/message")
async def post_message(payload: dict):
    """Receive a message and forward to agent service.

    TODO: replace payload: dict with Pydantic models from app.models.schemas
    """
    return {"status": "ok", "message": "router placeholder"}
