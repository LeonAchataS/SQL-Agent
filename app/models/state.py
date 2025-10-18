"""Internal state models for conversation flow."""

from pydantic import BaseModel
from typing import Dict, Any, List


class ConversationState(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]] = []
    collected_filters: Dict[str, Any] = {}
    required_remaining: List[str] = []
    optional_allowed: int = 3
